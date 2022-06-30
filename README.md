# Taipei-Day-Trip-Website (旅遊電商網站)

台北一日遊專案是一個使用者能夠查詢台北的景點並且預定行程的旅遊電商網站。

This website is a tourism e-commerce website where users can search the attractions in Taipei city and book travel itineraries.

- Website URL: https://taipeitrip-claire.online/
- Test account (測試帳號)
    - email: test1@gmail.com
    - password: test1
- Test credit card (測試信用卡)
    - Credit card : 4242-4242-4242-4242
    - Date: 01/23
    - CVV: 123

##  Technique
- Develop with **Python** using **Flask** framework.
- Deploy by **AWS EC2**.
- Use **Index** to facilitate query efficiencies in **MySQL**.
- Use **TapPay** SDK as payment system.
- Apply for **SSL** in Let's Encrypt.
- Use **JSON Web Token** to authenticate users.
- Make **RWD layout** and **Infinite Scroll** with pure JavaScript.


### Server Architecture
![image](https://user-images.githubusercontent.com/93002296/175474204-28128154-5f81-499c-95d4-1edd7f723529.png)

### Back-End Tech Stack
- Language / Web Framework 
  - Python / Flask
- Authentication
  - JSON Web Token (JWT)
  - werkzeug.security (Encode & Verify Password)
- Database
    - MySQL

### Front-End Tech Stack
- JavaScript 
- HTML
- CSS

### Network 
- NGINX 
  - Domain name system
  - Support HTTP & HTTPS

### Version Control
- Git/GitHub

## Demo / Main Function
### Home page:
- Search attractions by keyword or scroll down the scroll wheel to view all attractions.
![image](https://github.com/claire0613/gif/blob/main/taipei-index.gif)

### Booking System:
- Users can book the day and time on every attraction page, then fill out their contact information and pay the order by credit card. 
![image](https://user-images.githubusercontent.com/93002296/175504004-39ff1c7e-4807-4d79-a753-0037b811036e.png)

### Member System:
- Users can register, log in, log out of the website.
![image](https://user-images.githubusercontent.com/93002296/175494089-8d5c6187-acf2-444b-92c2-fc19d00aae19.png)
- Users can search historical orders and modify the username or the password.
![image](https://github.com/claire0613/gif/blob/main/taipei-member.gif)




## Contact
- 📞 Claire Liang
- 📧 claire0711@gmail.com




