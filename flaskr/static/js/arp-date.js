let formData = {};
console.log("test");

// Восстановление данных при загрузке страницы
window.onload = function() {
    if (formData.mac_address) document.getElementById('mac_address_input').value = formData.mac_address;
    if (formData.period_unit) document.getElementById('period_unit_input').value = formData.period_unit;
    if (formData.period_names) document.getElementById('period_names').value = formData.period_names;
};

// Сохранение данных в переменную при изменении
document.getElementById('mac_table_form').addEventListener('input', function() {
    formData.name = document.getElementById('mac_address_input').value;
    formData.email = document.getElementById('period_unit_input').value;
    formData.period_names = document.getElementById('period_names').value;
});