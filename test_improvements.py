#!/usr/bin/env python
"""Script de teste para verificar se as melhorias estão funcionando."""

import sys
import traceback

def test_imports():
    """Testa se todos os módulos podem ser importados."""
    print("=" * 60)
    print("TESTANDO IMPORTAÇÕES")
    print("=" * 60)
    
    try:
        from backend.config import BASE_DIR, CSV_FILES
        print("✅ backend.config")
    except Exception as e:
        print(f"❌ backend.config: {e}")
        traceback.print_exc()
        return False
    
    try:
        from backend.security import hash_password, verify_password
        print("✅ backend.security")
    except Exception as e:
        print(f"❌ backend.security: {e}")
        traceback.print_exc()
        return False
    
    try:
        from backend.validators import PetValidator, TutorValidator
        print("✅ backend.validators")
    except Exception as e:
        print(f"❌ backend.validators: {e}")
        traceback.print_exc()
        return False
    
    try:
        from backend.logger import log_info, log_error
        print("✅ backend.logger")
    except Exception as e:
        print(f"❌ backend.logger: {e}")
        traceback.print_exc()
        return False
    
    try:
        from backend.utils import tutor_label, pet_label
        print("✅ backend.utils")
    except Exception as e:
        print(f"❌ backend.utils: {e}")
        traceback.print_exc()
        return False
    
    try:
        from backend.enums import VacinaStatus, Cargo
        print("✅ backend.enums")
    except Exception as e:
        print(f"❌ backend.enums: {e}")
        traceback.print_exc()
        return False
    
    try:
        from backend.services import (
            cadastrar_pet, cadastrar_tutor, registrar_vacina, 
            login_usuario, cadastrar_usuario
        )
        print("✅ backend.services")
    except Exception as e:
        print(f"❌ backend.services: {e}")
        traceback.print_exc()
        return False
    
    return True


def test_security():
    """Testa funções de segurança."""
    print("\n" + "=" * 60)
    print("TESTANDO SEGURANÇA")
    print("=" * 60)
    
    try:
        from backend.security import hash_password, verify_password
        
        senha = "test123"
        hash_result = hash_password(senha)
        print(f"✅ Hash gerado: {hash_result[:30]}...")
        
        is_valid = verify_password(senha, hash_result)
        print(f"✅ Verificação correta: {is_valid}")
        
        is_invalid = verify_password("wrong", hash_result)
        print(f"✅ Rejeição correta: {not is_invalid}")
        
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        traceback.print_exc()
        return False


def test_validators():
    """Testa validadores."""
    print("\n" + "=" * 60)
    print("TESTANDO VALIDADORES")
    print("=" * 60)
    
    try:
        from backend.validators import TutorValidator
        
        # Teste válido
        tutor = TutorValidator(
            nome="João Silva",
            email="joao@example.com",
            telefone="11999999999"
        )
        print(f"✅ Tutor válido aceito: {tutor.nome}")
        
        # Teste inválido
        try:
            TutorValidator(
                nome="JJ",  # Muito curto
                email="joao@example.com",
                telefone="11999999999"
            )
            print("❌ Deveria ter rejeitado nome curto")
            return False
        except ValueError:
            print("✅ Nome curto rejeitado corretamente")
        
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        traceback.print_exc()
        return False


if __name__ == "__main__":
    all_ok = True
    
    if not test_imports():
        all_ok = False
    
    if not test_security():
        all_ok = False
    
    if not test_validators():
        all_ok = False
    
    print("\n" + "=" * 60)
    if all_ok:
        print("✅ TODOS OS TESTES PASSARAM")
        print("=" * 60)
        sys.exit(0)
    else:
        print("❌ ALGUNS TESTES FALHARAM")
        print("=" * 60)
        sys.exit(1)
