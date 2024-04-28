from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .forms import ContactForm
from .models import CustomPage, Blog
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .forms import BusinessInquiryForm
from openai import OpenAI
from decouple import config

def index(request):
    if request.method == 'POST':
        form = BusinessInquiryForm(request.POST)
        if form.is_valid():
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                print('form validation')
                inquiry = form.save(commit=False)
                # Optionally modify the interaction with the API based on ad_product
                # inquiry.user_description = ''
                # inquiry.ad_product = ''
                inquiry.save()
                user_description = 'sdasdadsasdasd'
                print('Success')
                print(request.headers)
                print(request.POST.dict()['ad_product'])
                # OpenAI ChatGPT ile iletişim kur
                api_key = config('API_KEY_AI')
                # new

                # Define the system prompt that includes the rules for each advertising platform
                system_prompt = config('PROMPT')
                print(api_key,system_prompt )
                prompt = config('PROMPT_SEC')
                client = OpenAI(

                    api_key=api_key,  # this is also the default, it can be omitted
                )
                # Assuming 'request' is your HTTP request object in a Django view
                user_description = request.POST.get('user_description')
                ad_product = request.POST.get('ad_product')
                chat_completion = client.chat.completions.create(
                    model="gpt-3.5-turbo-0125",
                    max_tokens=2000,
                    messages=[{"role": "system", "content": system_prompt},
                              {"role": "user", "content": "Business description: {0}".format(user_description)},
                              {'role': 'system', "content": prompt},
                             ]
                )

                print(chat_completion.choices[0].message.json())
                response_text = chat_completion.choices[0].message.dict()['content'].replace("html", "").replace("```", "")

                # response_text = 'dddd'
                response_data = {
                    'message': f'{response_text}'
                }
                return JsonResponse(response_data)
        else:
            # Output errors to see what's going wrong
            print(form.errors)  # This will print form errors to your console
            return JsonResponse({'status': 'error', 'errors': form.errors.as_json()})
    else:
        form = BusinessInquiryForm()
    return render(request, 'index.html', {'form': form})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! We will reach out to you as soon as possible.")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def custom_page(request, slug=None):
    content = get_object_or_404(CustomPage, slug=slug)
    return render(request, 'custom.html', {'content': content})


def blog(request):
    blog_list = Blog.objects.all().order_by('-publish')  # Assuming there's a date_posted field
    paginator = Paginator(blog_list, 10)  # Show 10 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog.html', {'page_obj': page_obj})


def blog_detail(request, slug=None):
    blogDetail = get_object_or_404(Blog, slug=slug)
    return render(request, 'blog_detail.html', {'post': blogDetail})


def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /admin/",
        "Allow: /",
        "Sitemap: https://www.reduceimagesizer.com/sitemap.xml"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
