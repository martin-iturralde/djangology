from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Character, Equipement


def post_list(request):
    characters = Character.objects.all()
    equipements = Equipement.objects.all()
    return render(request, 'blog/post_list.html', {'characters': characters, 'equipements': equipements})


def character_detail(request, id_character):
    message = ""
    error = None
    character = get_object_or_404(Character, id_character=id_character)
    form = MoveForm(request.POST, instance=character)
    lieu_avant = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
    
    if form.is_valid() and request.method == "POST":
        form.save(commit=False)
        nouveau_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip) 
        # Vrai
        if statut_match(nouveau_lieu.id_equip, character.etat) and nouveau_lieu.disponibilite == "libre":
            lieu_avant.disponibilite = "libre"
            error = False
            actualiser_disponibilite(nouveau_lieu)
            lieu_avant.save()
            form.save() 
            mise_statut(nouveau_lieu, character)
            message = "modification réussie"
        # Faux
        else:
            error = True
            message = "modification non réussie"
        return render(request,
                  'blog/character_detail.html',
                  {'character': character, 'message': message, 'error': error, 'lieu': lieu_avant, 'new_lieu':nouveau_lieu, 'form': form})

    else:
        form = MoveForm()
        return render(request,
                  'blog/character_detail.html',
                  {'character': character, 'message': message, 'lieu': lieu_avant, 'form': form})


def statut_match(nouveau_lieu_name, character_etat):
    if character_etat == "affame" and nouveau_lieu_name == "mangeoire":
        return True
    elif character_etat == "fatigue" and nouveau_lieu_name == "nid":
        return True
    elif character_etat == "repus" and nouveau_lieu_name == "roue":
        return True
    elif character_etat == "endormi" and nouveau_lieu_name == "litiere":
        return True
    else:
        return False


def mise_statut(lieu, character):
    if lieu.id_equip == "mangeoire":
        character.etat = "repus"
    elif lieu.id_equip == "nid":
        character.etat = "endormi"    
    elif lieu.id_equip == "roue":
        character.etat = "fatigue"
    elif lieu.id_equip == "litiere":
        character.etat = "affame"   
    character.save()


def actualiser_disponibilite(lieu):
    if lieu.id_equip == "litiere":
        lieu.disponibilite = "libre"
    elif lieu.id_equip in ["roue", "mangeoire", "nid"]:
        lieu.disponibilite = "occupe"
    lieu.save()