@echo off
setlocal enabledelayedexpansion

REM Base URL of your API
@REM set BASE_URL=http://127.0.0.1:8080
set BASE_URL=db-group5-452710.wl.r.appspot.com

REM Seller
echo ==== Register Seller ====
curl -X POST -H "Content-Type: application/json" ^
  -d "{\"username\":\"test_seller\",\"password\":\"seller123\",\"email\":\"seller@example.com\",\"store_name\":\"Test Store\",\"business_license\":\"LIC123456\"}" ^
  %BASE_URL%/register/seller

echo.

echo ==== Login Seller ====
curl -X POST -H "Content-Type: application/json" ^
  -d "{\"username\":\"test_seller\",\"password\":\"seller123\"}" ^
  %BASE_URL%/login/seller

echo.

REM Admin
echo ==== Register Admin ====
curl -X POST -H "Content-Type: application/json" ^
  -d "{\"username\":\"test_admin\",\"password\":\"admin123\",\"email\":\"admin@example.com\",\"admin_level\":\"2\"}" ^
  %BASE_URL%/register/admin

echo.

echo ==== Login Admin ====
curl -X POST -H "Content-Type: application/json" ^
  -d "{\"username\":\"test_admin\",\"password\":\"admin123\"}" ^
  %BASE_URL%/login/admin

echo.

REM Customer
echo ==== Register Customer ====
curl -X POST -H "Content-Type: application/json" ^
  -d "{\"username\":\"test_customer\",\"password\":\"cust123\",\"email\":\"customer@example.com\",\"first_name\":\"Alice\",\"last_name\":\"Wang\",\"phone\":\"1234567890\"}" ^
  %BASE_URL%/register/customer

echo.

echo ==== Login Customer ====
curl -X POST -H "Content-Type: application/json" ^
  -d "{\"username\":\"test_customer\",\"password\":\"cust123\"}" ^
  %BASE_URL%/login/customer

echo.
pause
