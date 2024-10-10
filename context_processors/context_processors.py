from cart.cart_module import Cart
from blog.models import Post

def recent_posts(request):
    recent_posts = Post.objects.all().order_by('-created_at')[:3]

    return {'recent_posts': recent_posts}




def cart_count(request):
    cart = Cart(request)
    return {'cart_count': cart.get_total_quantity()}
