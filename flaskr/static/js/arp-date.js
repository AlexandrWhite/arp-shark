window.onload = function(){
    console.log('xx');
    document.getElementById('mac_table_form').addEventListener('submit', function(event) {
        console.log(document.getElementById('mac-address_input').value);
    })
};