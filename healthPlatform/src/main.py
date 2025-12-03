def main_menu():
    print("\n=== SISTEMA CLÍNICA VIDA+ ===")
    print("1. Cadastrar paciente")
    print("2. Buscar paciente")
    print("3. Ver estatísticas")
    print("4. Fila de atendimento")
    print("5. Listar todos os pacientes")
    print("6. Gerenciar agendamentos")
    print("7. Gerenciar atendimentos")
    print("8. Sair")

def main():
    from controllers.patient_controller import PatientController
    from controllers.queue_controller import QueueController
    from controllers.appointment_controller import AppointmentController
    from controllers.attendance_controller import AttendanceController

    patient_controller = PatientController()
    queue_controller = QueueController()
    appointment_controller = AppointmentController()
    attendance_controller = AttendanceController()

    while True:
        main_menu()
        choice = input("Escolha uma opção: ").strip()
        if choice == '1':
            patient_controller.register_patient()
        elif choice == '2':
            patient_controller.search_patient()
        elif choice == '3':
            patient_controller.view_statistics()
        elif choice == '4':
            queue_controller.attend_next_patient()
        elif choice == '5':
            patient_controller.list_patients()
        elif choice == '6':
            appointment_controller.manage_menu()
        elif choice == '7':
            attendance_controller.manage_menu()
        elif choice == '8':
            print("Saindo... Até logo.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()