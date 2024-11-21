window.onload = function(){
    var mac_input = document.getElementById('mac-address_input');
    var period_name_input = document.getElementById('period-names');
    var period_unit_input = document.getElementById('period-unit_input');

    if(localStorage.getItem('mac') !== null){
        mac_input.value = localStorage.getItem('mac');
    }

    if(localStorage.getItem('period_name') !== null){
        period_name_input.value = localStorage.getItem('period_name');
    }

    if(localStorage.getItem('period_unit') !== null){
        period_unit_input.value = localStorage.getItem('period_unit');
    }

    document.getElementById('mac_table_form').addEventListener('submit', function(event) {
        localStorage.setItem('mac',mac_input.value);
        localStorage.setItem('period_name',period_name_input.value);
        localStorage.setItem('period_unit',period_unit_input.value);
        console.log(document.getElementById('mac-address_input').value);
    })
};