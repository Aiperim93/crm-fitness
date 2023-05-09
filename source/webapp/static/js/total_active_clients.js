import {activeClients} from "./config.js";


document.addEventListener('DOMContentLoaded', async function () {
    const datePicker = document.getElementById('date-picker');
    const submitBtn = document.getElementById('submit-btn');
    const totalCount = document.getElementById('total-count');


    const today = new Date();
    const day = today.getDate().toString().padStart(2, '0');
    const month = (today.getMonth() + 1).toString().padStart(2, '0');
    const year = today.getFullYear();
    const todayString = `${year}-${month}-${day}`;


    datePicker.value = todayString;

    async function getTotalCount(date) {
        let url = activeClients;
        if (date) {
            url += '?date=' + date;
        }
        try {
            const response = await fetch(url);
            const data = await response.json();
            return data.count;
        } catch (error) {
            console.error(error);
        }
    }

    const todayCount = await getTotalCount(todayString);
    totalCount.innerText = todayCount;

    submitBtn.addEventListener('click', async function () {
        const date = datePicker.value;
        const count = await getTotalCount(date);
        totalCount.innerText = count;
    });
});