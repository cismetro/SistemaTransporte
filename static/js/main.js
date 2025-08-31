// Funções JavaScript básicas
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts após 5 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
    
    // Máscara para CPF
    const cpfInputs = document.querySelectorAll('input[name="cpf"]');
    cpfInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
            e.target.value = value;
        });
    });
    
    // Máscara para telefone
    const phoneInputs = document.querySelectorAll('input[name="phone"], input[name="emergency_phone"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/(\d{2})(\d)/, '($1) $2');
            value = value.replace(/(\d)(\d{4})$/, '$1-$2');
            e.target.value = value;
        });
    });
});

// Função para buscar paciente por CPF
function searchPatientByCPF(cpf) {
    if (cpf.length >= 11) {
        fetch(`/patients/search?cpf=${cpf}`)
            .then(response => response.json())
            .then(data => {
                if (data.found) {
                    document.getElementById('patient_id').value = data.id;
                    document.getElementById('patient_name').value = data.name;
                    if (data.special_needs) {
                        document.getElementById('observations').value = 'Necessidades especiais: ' + data.special_needs;
                    }
                } else {
                    alert('Paciente não encontrado. Verifique o CPF ou cadastre o paciente primeiro.');
                }
            })
            .catch(error => {
                console.error('Erro:', error);
            });
    }
}