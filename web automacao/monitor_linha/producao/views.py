from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ParadasLinha, MotivosParadas

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

        MotivosParadas.objects.create(
            nome_linha=nome_linha,
            inicio_parada=inicio_parada,
            fim_parada=fim_parada if fim_parada != "None" else None,
            motivo=motivo,
        )
        return JsonResponse({"status": "ok"})

    return JsonResponse({"status": "erro"}, status=400)
