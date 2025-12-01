from datetime import datetime, timedelta
from collections import defaultdict

def get_dashboard_chart_data(usuario_ativo):
    """
    Agrega dados para os gráficos do dashboard baseados no representante ativo.
    
    Args:
        usuario_ativo: O objeto Representante ativo.
        
    Returns:
        Um dicionário contendo rótulos e valores para 'msg_chart' e 'student_chart'.
    """
    
    # --- Lógica de Intervalo de Datas ---
    # Determinar data de início: usar data de criação dos metadados, ou hoje se ausente
    start_date_str = usuario_ativo.metadata.get('created_at')
    if start_date_str:
        try:
            # Tratar formato "dd/mm/YYYY HH:MM:SS" (usado no controle_db.py)
            start_date = datetime.strptime(start_date_str, "%d/%m/%Y %H:%M:%S")
        except ValueError:
             # Fallback se formato for inesperado
            start_date = datetime.now()
    else:
         # Fallback se não houver metadados
        start_date = datetime.now()
    
    end_date = datetime.now()
    
    # Normalizar para objetos date (remove hora e timezone)
    # Isso corrige o erro "can't compare offset-naive and offset-aware datetimes"
    start_date = start_date.date()
    end_date = end_date.date()
    
    # Gerar todas as datas no intervalo
    all_dates = []
    current_date = start_date
    while current_date <= end_date:
        all_dates.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
        
    # Garantir que pelo menos hoje esteja presente se o intervalo estiver vazio (ex: criado agora)
    if not all_dates:
        all_dates.append(end_date.strftime("%Y-%m-%d"))

    # --- 1. Mensagens por Dia ---
    msgs_per_day = defaultdict(int)
    for msg in usuario_ativo.mensagens:
        # formato msg['data']: "dd/mm/YYYY HH:MM:SS"
        try:
            dt = datetime.strptime(msg['data'], "%d/%m/%Y %H:%M:%S")
            date_str = dt.strftime("%Y-%m-%d")
            msgs_per_day[date_str] += 1
        except ValueError:
            continue
    
    # Preencher todas as datas com 0 se não houver mensagens
    msg_chart_values = [msgs_per_day[d] for d in all_dates]

    # --- 2. Representados por Dia ---
    students_per_day = defaultdict(int)
    for aluno in usuario_ativo.alunos:
        # formato aluno.data_adicionado: formato ISO "YYYY-MM-DDTHH:MM:SS.ssssss"
        if aluno.data_adicionado:
            try:
                # Tratar formato ISO (pode conter 'T' ou espaço)
                dt = datetime.strptime(aluno.data_adicionado, "%d/%m/%Y %H:%M:%S")
                dt_str = dt.strftime("%Y-%m-%d")
                students_per_day[dt_str] += 1
            except Exception:
                continue
    
    student_chart_values = [students_per_day[d] for d in all_dates]

    # --- 3. Novos Representados nos Últimos 7 Dias ---
    new_students_last_7_days = 0
    seven_days_ago = datetime.now() - timedelta(days=7)
    for aluno in usuario_ativo.alunos:
        if aluno.data_adicionado:
            try:
                # Tratar formato ISO
                dt = datetime.fromisoformat(aluno.data_adicionado)
                if dt >= seven_days_ago:
                    new_students_last_7_days += 1
            except ValueError:
                continue

    return {
        'msg_chart_labels': all_dates,
        'msg_chart_values': msg_chart_values,
        'student_chart_labels': all_dates,
        'student_chart_values': student_chart_values,
        'new_students_last_7_days': new_students_last_7_days
    }
