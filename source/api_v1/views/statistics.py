from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from webapp.models import Training, Payment, GroupTraining, LazyDays
from django.db.models import Count, Sum
from django.http import JsonResponse


class StaticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        try:
            if start_date > end_date:
                return JsonResponse({'error': 'Start_date cannot be greater than end_date'}, status=400)
            else:
                visits = Training.objects.filter(date__range=(start_date, end_date)).values('date').annotate(
                    count=Count('id'))

                payments = Payment.objects.filter(paid_at__date__lte=end_date, paid_at__date__gte=start_date).values(
                    'paid_at__date').annotate(
                    total_amount=Sum('amount'), total_count=Count('id'))

                lazy_days = LazyDays.objects.filter(start_date__range=(start_date, end_date),
                                                    end_date__range=(start_date, end_date)).values('start_date',
                                                                                                   'end_date')
                lazy_days_data = list(lazy_days)

                missing_count = {}

                group_trainings = GroupTraining.objects.filter(created_at__date__range=(start_date, end_date))
                for group_training in group_trainings:
                    active_clients = group_training.group.clients.active_clients()
                    for client in active_clients:
                        training = client.trainings.filter(date=group_training.created_at.date()).first()
                        if not training:
                            date_str = str(group_training.created_at.date())
                            missing_count[date_str] = missing_count.get(date_str, 0) + 1

                data = {}
                date_range = (datetime.strptime(start_date, '%Y-%m-%d'), datetime.strptime(end_date, '%Y-%m-%d'))
                for n in range(int((date_range[1] - date_range[0]).days) + 1):
                    date = (date_range[0] + timedelta(n)).strftime("%Y-%m-%d")
                    data[date] = {'visits': 0, 'total_amount': 0, 'total_count': 0, 'missing_count': 0, 'total_lazy_day': 0}

                for visit in visits:
                    data[visit['date'].strftime("%Y-%m-%d")]['visits'] = visit['count']

                for payment in payments:
                    data[payment['paid_at__date'].strftime("%Y-%m-%d")]['total_amount'] = payment['total_amount']
                    data[payment['paid_at__date'].strftime("%Y-%m-%d")]['total_count'] = payment['total_count']

                for lazy_day in lazy_days_data:
                    start_date = lazy_day['start_date'].strftime("%Y-%m-%d")
                    end_date = lazy_day['end_date'].strftime("%Y-%m-%d")
                    for n in range(int((datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(
                            start_date, '%Y-%m-%d')).days) + 1):
                        date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(n)).strftime("%Y-%m-%d")
                        data[date]['total_lazy_day'] += 1

                for date_str, count in missing_count.items():
                    data[date_str]['missing_count'] = count

            return JsonResponse(data, safe=False)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
