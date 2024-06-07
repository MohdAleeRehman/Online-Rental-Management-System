from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Item, RentalRequest, Profile
from .forms import ItemForm
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm
from django.db.models import Q
from django.contrib import messages


@login_required
def item_list(request):
    items = Item.objects.filter(status="available")
    return render(request, "rentals/item_list.html", {"items": items})


@login_required
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, "rentals/item_detail.html", {"item": item})


@login_required
def add_item(request):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            messages.success(request, "Item added successfully.")
            return redirect("item_list")
        else:
            messages.error(
                request, "There was an error adding your item. Please try again."
            )
    else:
        form = ItemForm()
    return render(request, "rentals/add_item.html", {"form": form})


@login_required
def request_rental(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        # Create the rental request
        RentalRequest.objects.create(
            item=item, requester=request.user, status="requested"
        )
        item.status = "requested"
        item.save()
        messages.success(request, "Rental request submitted.")
        return redirect("item_list")
    return render(request, "rentals/request_rental.html", {"item": item})


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get("first_name")
            user.profile.last_name = form.cleaned_data.get("last_name")
            user.profile.phone_number = form.cleaned_data.get("phone_number")
            user.save()
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect("item_list")
        else:
            messages.error(
                request, "There was an error with your registration. Please try again."
            )
    else:
        form = UserRegistrationForm()
    return render(request, "rentals/register.html", {"form": form})


@login_required
def profile(request):
    rental_requests = RentalRequest.objects.filter(
        requester=request.user
    ).select_related("item", "item__owner")
    owned_items = Item.objects.filter(owner=request.user).prefetch_related(
        "rental_requests__requester"
    )
    return render(
        request,
        "rentals/profile.html",
        {
            "rental_requests": rental_requests,
            "owned_items": owned_items,
        },
    )


@login_required
def user_profile(request, user_id):
    user_profile = get_object_or_404(Profile, user__id=user_id)
    owned_items = Item.objects.filter(owner=user_profile.user).prefetch_related(
        "rental_requests__requester"
    )
    return render(
        request,
        "rentals/user_profile.html",
        {
            "user_profile": user_profile,
            "owned_items": owned_items,
        },
    )


@login_required
def search_items(request):
    query = request.GET.get("q")
    print(f"Query: {query}")

    if query:
        items = Item.objects.filter(
            (
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(keywords__icontains=query)
            )
            & Q(status="available")
        ).exclude(owner=request.user)

        print(f"Items (Filtered Query): {[item.name for item in items]}")
    else:
        items = Item.objects.none()
    return render(
        request, "rentals/search_results.html", {"items": items, "query": query}
    )


@login_required
def cancel_request(request, pk):
    rental_request = get_object_or_404(
        RentalRequest, pk=pk, requester=request.user, status="requested"
    )
    rental_request.delete()
    rental_request.item.status = "available"
    rental_request.item.save()
    messages.success(request, "Rental request cancelled.")
    return redirect("profile")


@login_required
def manage_items(request):
    owned_items = request.user.owned_items.all()
    return render(request, "rentals/manage_items.html", {"owned_items": owned_items})


@login_required
def update_item_status(request, pk, status):
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    if status == "rented":
        rental_request = item.rental_requests.filter(status="requested").first()
        if rental_request:
            rental_request.status = "rented"
            rental_request.save()
            messages.success(request, "Item marked as rented.")
        else:
            messages.error(request, "No rental requests for this item.")
    elif status == "available":
        rental_request = item.rental_requests.filter(status="rented").first()
        if rental_request:
            rental_request.is_completed = True
            rental_request.status = "returned"
            rental_request.save()
            messages.success(request, "Item marked as available.")

    item.status = status
    item.save()
    messages.success(request, "Item status updated.")
    return redirect("manage_items")


@login_required
def confirm_return(request, rental_request_id):
    rental_request = get_object_or_404(RentalRequest, pk=rental_request_id)
    if rental_request.item.owner == request.user:
        rental_request.is_completed = True
        rental_request.status = "returned"
        rental_request.item.status = "available"
        rental_request.item.save()
        rental_request.save()
        messages.success(request, "Item return confirmed.")
    else:
        rental_request.is_completed = True
        rental_request.status = "returned"
        rental_request.item.status = "available"
        rental_request.item.save()
        rental_request.save()
        messages.success(request, "Rented item has been returned to the owner, thank you!")
    return redirect("profile")
