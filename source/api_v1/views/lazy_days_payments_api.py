from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from webapp.manager import ActiveClientManager
from webapp.models import Client, Payment, LazyDays
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime


class LazyDaysAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        today = timezone.now().date()
        pk = self.kwargs.get('pk')
        client = Client.objects.get(pk=pk)
        active_payment = ActiveClientManager().active_payment(client)
        start_date = datetime.strptime(request.data['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.data['end_date'], '%Y-%m-%d').date()
        delta = end_date - start_date

        if start_date < today:
            return JsonResponse({'error': 'Start_date cannot be in the past'}, status=400)
        try:
            if start_date > end_date:
                return JsonResponse({'error': 'Start_date cannot be greater than end_date'}, status=400)
            else:
                try:
                    lazy_days = LazyDays.objects.create(payment=active_payment, start_date=start_date,
                                                        end_date=end_date)
                    if lazy_days:
                        payments = Payment.objects.filter(client=client)
                        future_payments = payments.filter(id__gt=active_payment.id)
                        active_payment.payment_end_date += delta
                        active_payment.save()
                        for payment in future_payments:
                            payment.payment_start_date += delta
                            payment.payment_end_date += delta
                            payment.save()
                        return JsonResponse({'status': 'Created lazy days'}, status=201)
                    else:
                        return JsonResponse({'error': 'Could not create lazy days'}, status=400)
                except Exception as e:
                    return JsonResponse({'error': str(e)}, status=500)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
