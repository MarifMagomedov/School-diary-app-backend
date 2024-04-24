# Эндпоинты

## 1. GET /auth/current_user
Запрос для получения текущего юзера
```json
{
  
}
```

## 2. POST /auth/register
Запрос на создание профиля, при неверно введеном пригласительном id юзера возвращется 400 код ошибки, если юзер уже проходил регистрацию - возвращается 409 код

Получаемые данные

```json
{
    "user_type": "string",
    "user_id": "string",
    "email": "string",
    "password": "string",
    "vk": null,
    "telegram": null
}
```
Возвращаемые данные
```json lines
// 201
{
    'message': 'Account created successfully'
}
```
```json lines
// 400
{
    "message": "Invalid user id for register user"
}
```
```json lines
//409
{
    "message": "User already registered"
}
```

## 3. POST /auth/login
```json
{
  
}
```
## 4. GET /teachers/{id: int}/subjects
Запрос на получение предметов, преподаваемых учителем
```json
{
  
}
```

## 5. GET /teachers/{id: int}/classes
Запрос на получение классов, обучаемых у данного учителя
```json
{
  
}
```

## 6. GET /class/{id: int}/students
Запрос на получение учеников, учащихся в данном классе
```json
{
  
}
```

## 7. GET /teachers/all
Запрос на получение всех учителей, преподающих в школе
```json
{
  
}
```

## 8. GET /classes/all
Запрос на получение всех учителей, преподающих в школе
```json
{
  
}
```

## 9. GET /subjects/all
Запрос на получение всех учителей, преподающих в школе
```json
{
  
}
```
