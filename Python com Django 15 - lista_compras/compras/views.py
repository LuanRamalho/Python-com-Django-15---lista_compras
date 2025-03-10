from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa
from .models import Nota, Item
from .forms import NotaForm, ItemForm

def lista_notas(request):
    notas = Nota.objects.all()
    return render(request, 'compras/lista_notas.html', {'notas': notas})

def criar_nota(request):
    if request.method == 'POST':
        form = NotaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_notas')
    else:
        form = NotaForm()
    return render(request, 'compras/criar_nota.html', {'form': form})

def visualizar_nota(request, nota_id):
    nota = get_object_or_404(Nota, id=nota_id)
    itens = Item.objects.filter(nota=nota)
    total_geral = round(sum(item.sub_total for item in itens), 2)  # Garantir arredondamento correto
    return render(request, 'compras/visualizar_nota.html', {'nota': nota, 'itens': itens, 'total_geral': total_geral})

def adicionar_item(request, nota_id):
    nota = get_object_or_404(Nota, id=nota_id)
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.nota = nota
            item.save()
            return redirect('visualizar_nota', nota_id=nota.id)
    else:
        form = ItemForm()
    return render(request, 'compras/adicionar_item.html', {'form': form, 'nota': nota})

def editar_nota(request, nota_id):
    nota = get_object_or_404(Nota, id=nota_id)
    if request.method == 'POST':
        form = NotaForm(request.POST, instance=nota)
        if form.is_valid():
            form.save()
            return redirect('lista_notas')
    else:
        form = NotaForm(instance=nota)
    return render(request, 'compras/editar_nota.html', {'form': form, 'nota': nota})

def excluir_nota(request, nota_id):
    nota = get_object_or_404(Nota, id=nota_id)
    if request.method == 'POST':
        nota.delete()
        return redirect('lista_notas')
    return render(request, 'compras/excluir_nota.html', {'nota': nota})

def editar_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('visualizar_nota', nota_id=item.nota.id)
    else:
        form = ItemForm(instance=item)
    return render(request, 'compras/editar_item.html', {'form': form, 'item': item})

def excluir_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    nota_id = item.nota.id
    if request.method == 'POST':
        item.delete()
        return redirect('visualizar_nota', nota_id=nota_id)
    return render(request, 'compras/excluir_item.html', {'item': item})

def comparar_precos(request, nota_id):
    nota = get_object_or_404(Nota, id=nota_id)
    if request.method == 'POST':
        nota.anotacao_precos = request.POST.get('anotacao_precos', '')
        nota.save()
        return redirect('visualizar_nota', nota_id=nota.id)
    return render(request, 'compras/comparar_precos.html', {'nota': nota})

def gerar_pdf_precos(request, nota_id):
    nota = get_object_or_404(Nota, id=nota_id)
    
    # Renderize o template como HTML
    context = {'nota': nota}
    html = render_to_string('compras/pdf_precos.html', context)
    
    # Crie a resposta HTTP para o arquivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="comparacao_precos_{nota_id}.pdf"'
    
    # Converta o HTML em PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # Retorne a resposta com o arquivo PDF gerado
    if pisa_status.err:
        return HttpResponse('Erro ao gerar o PDF', status=500)
    
    return response
