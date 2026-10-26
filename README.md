# Internet Magazin API 

Django REST Framework va Redis asosida qurilgan elektron tijorat (E-commerce) va mahsulotlarni boshqarish tizimi API’si.

## 🚀 Asosiy Imkoniyatlar va Texnologiyalar
- **Python / Django / Django REST Framework (DRF):** Asosiy backend arxitekturasi va RESTful API'lar.
- **PostgreSQL:** Ma'lumotlar bazasi.
- **Redis:** 
  * Mahsulotlar ro'yxatini tezkor keshilash (`django-redis`).
  * Real vaqt rejimida mahsulot ko'rishlar sonini kuzatish (`views_count`).
  * Foydalanuvchilar uchun vaqtinchalik savat (Temporary Cart) tizimi.
- **Docker & Docker Compose:** To'liq konteynerizatsiya qilingan muhit.
- **Swagger & ReDoc:** Avtomatlashtirilgan API hujjatlari.

---

## 🛠 1. O'rnatish va Ishga Tushirish (Docker orqali)

1. Repozitoriyani klon qilib oling:
   ```bash
   git clone [https://github.com/ilhomjon-ahmadjonov/internet_magazin-api.git](https://github.com/ilhomjon-ahmadjonov/internet_magazin-api.git)
   cd internet_magazin-api
