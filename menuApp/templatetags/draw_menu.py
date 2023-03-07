#  Django модули
from django.db import connection
from django import template
#  Модули проекта
from menuApp.models import Menu

#  Модуль подсчёта времени выполнения функции 
from time import perf_counter



register = template.Library()
@register.simple_tag()
def draw_menu(name : str):
    #  Отсчёт времени начала функции
    start = perf_counter()
    #  Очистка списка запросов
    connection.queries.clear()
    #  Получение текущего меню, его предка и его детей
    current_menu = Menu.objects.select_related(
        'parent'
    ).prefetch_related('children').get(pk=name)
    #  Получение главного предка текущего меню
    top_ancestor = current_menu.parent or current_menu
    #  Получение списка 
    parents = [top_ancestor,]
    while top_ancestor.parent:
        parents.append(top_ancestor)
        top_ancestor = top_ancestor.parent
        
    def build_menu(menu : Menu) -> str:
        #  Рендер главного родителя
        builded_menu = '<li><a href="/{}"{}>{}</a>'.format(menu.pk, 'class="active"' if current_menu == menu else '', menu.title, )
        #  Рендер детей главного родителя
        builded_menu += build_menu_skeleton(menu.children.all(), depth=0)
        return builded_menu
    
    def build_menu_skeleton(items : list[Menu], depth : int) -> str:
        menu = ''
        #  Максимальная глубина всего меню
        max_depth = len(parents)
        #  Предки выбранного меню
        ancestors = parents[2:] + [parents[-1]] + [current_menu.parent] 
        #  Дети выбранного меню
        children = parents + list(current_menu.children.all())
        for item in items:
            #  Если элемент - выбранное меню, добавляем сам элемент и активный класс нему
            if item == current_menu:
                menu += '<li class="list-group-item"><a class="active" href="/{0}">{1}</a></li>'.format(item.pk, item.title)
                #  Проверяем, есть ли у выбранного меню дочерние элементы
                if item.children.exists() and depth < max_depth:
                    other = build_menu_skeleton(item.children.all(), depth+1)
                    if other:
                        menu += '<ul>{}</ul>'.format(other)
            #  Проверка на то, является ли элемент страной
            elif item.parent == parents[-1].parent:
                menu += '<li class="list-group-item"><a href="/{0}">{1}</a></li>'.format(item.id, item.title)
            # Если элемент находится в предках выбранного меню или является его потомком
            elif item.parent in ancestors or item in children:
                menu += '<li class="list-group-item"><a href="/{0}">{1}</a></li>'.format(item.id, item.title)
            #  Если у элемента есть дочерние элементы и глубина меню не превышает максимальной, то вызываем рекурсию  
            if item in parents and depth < max_depth:
                other = build_menu_skeleton(item.children.all(), depth+1)
                if other:
                    menu += '<ul>{}</ul>'.format(other)
                
        return menu
    #  Подсчёт количества запросов в базу данных с момента начала функции
    num_queries = len(connection.queries)
    menu = build_menu(top_ancestor)
    #  Рендер статистики функции
    stat = f"<h1>Количество запросов: {num_queries} <br> Времени затрачено на рендер дерева: {int((perf_counter() - start) * 1000)} мс.</h1>" 
    return stat + menu
