let formData = {};
console.log("test");

document.addEventListener("DOMContentLoaded", function()  {
    if (formData.mac_address) document.getElementById('mac_address_input').value = localStorage.getItem('mac_address');
   
    document.getElementById('mac_table_form').addEventListener('submit', function(event){
        localStorage.setItem('mac_address',document.getElementById('mac_address_input').value);
    });    

});



