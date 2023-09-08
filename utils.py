from forms import LoginForm, RegistrationForm
# Название магазина
shop_name = 'Company Name'
# телефон поддержки
support_phone = '+7 (000) 000-00-00'
# основное меню в шапке
menu_header = [{'title': 'Магазин', 'url_name': '/'},
               {'title': 'Контакты', 'url_name': 'contacts'}]
# основное меню в шапке
menu_footer = [{'title': 'Политика конфиденциальности', 'url_name': 'privacy-policy'},
        {'title': 'Пользовательское соглашение', 'url_name': 'user-agreement'},
        {'title': 'Контакты', 'url_name': 'contacts'}]
# города обслуживания
city = 'Москва'
# категории меню товаров
categories = [{'id': 1, 'name': 'ЗАВТРАКИ', 'slug': 'breakfasts'},
              {'id': 2, 'name': 'САЛАТЫ', 'slug': 'salads'},
              {'id': 3, 'name': 'ПЕРВОЕ', 'slug': 'first'},
              {'id': 4, 'name': 'ВТОРОЕ', 'slug': 'second'},
              {'id': 5, 'name': 'ДЕСЕРТЫ', 'slug': 'desserts'},
              {'id': 6, 'name': 'ВЫПЕЧКА', 'slug': 'pastry'}]
