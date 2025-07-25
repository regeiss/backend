from django.core.exceptions import ValidationError
import re

def validate_cpf(cpf):
    """Valida CPF brasileiro"""
    if not cpf or len(cpf) != 11:
        raise ValidationError('CPF deve ter 11 dígitos')
    
    if not cpf.isdigit():
        raise ValidationError('CPF deve conter apenas números')
    
    # Validação do algoritmo do CPF
    if cpf == cpf[0] * 11:  # CPFs com todos os dígitos iguais
        raise ValidationError('CPF inválido')
    
    # Cálculo dos dígitos verificadores
    def calculate_digit(cpf_part, weights):
        total = sum(int(digit) * weight for digit, weight in zip(cpf_part, weights))
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder
    
    first_digit = calculate_digit(cpf[:9], range(10, 1, -1))
    second_digit = calculate_digit(cpf[:10], range(11, 1, -1))
    
    if cpf[-2:] != f"{first_digit}{second_digit}":
        raise ValidationError('CPF inválido')
    
    return cpf

def validate_cep(cep):
    """Valida CEP brasileiro"""
    if not re.match(r'^\d{8}$', cep):
        raise ValidationError('CEP deve ter 8 dígitos numéricos')
    return cep
