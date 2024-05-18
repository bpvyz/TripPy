document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('searchInput').addEventListener('input', function () {
        let input = this.value.toLowerCase();
        let table = document.getElementById('businessTable');
        let rows = table.getElementsByTagName('tr');
        for (let i = 0; i < rows.length; i++) {
            let cell = rows[i].getElementsByTagName('td')[1];
            if (cell) {
                let textValue = cell.textContent || cell.innerText;
                if (textValue.toLowerCase().indexOf(input) > -1) {
                    rows[i].style.display = '';
                } else {
                    rows[i].style.display = 'none';
                }
            }
        }
    });
});
