from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ParadasLinha, MotivosParadas
import csv
from datetime import datetime, timedelta

def tabela_paradas(request):
    paradas = ParadasLinha.objects.all().order_by("-inicio_parada")
    return render(request, 'producao/tabela_paradas.html', {'paradas': paradas})

@csrf_exempt
def registrar_motivo(request):
    if request.method == "POST":
        nome_linha = request.POST.get("nome_linha")
        inicio_parada = request.POST.get("inicio_parada")
        fim_parada = request.POST.get("fim_parada")
        motivo = request.POST.get("motivo")

        # Criar na tabela de motivos
        MotivosParadas.objects.create(
            nome_linha=nome_linha,
            inicio_parada=inicio_parada,
            fim_parada=fim_parada if fim_parada != "None" else None,
            motivo=motivo,
        )

        # Remover da tabela de paradas
        ParadasLinha.objects.filter(
            nome_linha=nome_linha,
            inicio_parada=inicio_parada,
            fim_parada=fim_parada if fim_parada != "None" else None
        ).delete()

        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "erro"}, status=400)


def exportar_csv(request, filtro):
    hoje = datetime.now()
    
    # Define a data de início de acordo com o filtro
    if filtro == "7dias":
        inicio = hoje - timedelta(days=7)
    elif filtro == "1mes":
        inicio = hoje - timedelta(days=30)
    elif filtro == "6meses":
        inicio = hoje - timedelta(days=180)
    elif filtro == "1ano":
        inicio = hoje - timedelta(days=365)
    else:
        inicio = None

    def parse_datetime(dt_str):
        try:
            return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        except:
            return None

    registros = MotivosParadas.objects.all()
    if inicio:
        registros = [r for r in registros 
                     if parse_datetime(str(r.inicio_parada)) and parse_datetime(str(r.inicio_parada)) >= inicio]

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="motivos_paradas_{filtro}.csv"'

    # Usando ; como separador para Excel em PT-BR
    writer = csv.writer(response, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["ID", "Nome da Linha", "Inicio da Parada", "Fim da Parada", "Motivo"])
    
    for r in registros:
        writer.writerow([
            r.id,
            str(r.nome_linha),
            str(r.inicio_parada),
            str(r.fim_parada) if r.fim_parada else "",
            str(r.motivo)
        ])

    return response
# views.py
