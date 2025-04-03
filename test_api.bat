@echo off
set BASE_URL=http://127.0.0.1:8080

echo === Cleaning up existing records ===
echo Deleting PRODUCT 'p456' if exists...
curl -X DELETE %BASE_URL%/product/p456
echo.
echo Deleting SELLER 'u123' if exists...
curl -X DELETE %BASE_URL%/seller/u123
echo.
echo Deleting CATEGORY 'c101' if exists...
curl -X DELETE %BASE_URL%/category/c101
echo.
echo Deleting USER 'u123' if exists...
curl -X DELETE %BASE_URL%/user/u123
echo.
echo --------------------------
echo Press any key to continue with tests...
pause

echo === Creating a new USER record ===
curl -X POST -H "Content-Type: application/json" -d "{\"user_id\": \"u123\", \"username\": \"u_123\", \"password\": \"secret\", \"email\": \"u123@example.com\"}" %BASE_URL%/user
echo.
echo --------------------------

echo === Creating a new SELLER record (pre-requisite for PRODUCT) ===
curl -X POST -H "Content-Type: application/json" -d "{\"user_id\": \"u123\", \"store_name\": \"John's Store\", \"business_license\": \"BL99999\"}" %BASE_URL%/seller
echo.
echo --------------------------

@REM echo === Creating a new CATEGORY record (pre-requisite for PRODUCT) ===
@REM curl -X POST -H "Content-Type: application/json" -d "{\"category_id\": \"c101\", \"category_name\": \"Electronics\", \"description\": \"Electronic gadgets and devices\"}" %BASE_URL%/category
@REM echo.
@REM echo --------------------------

echo === Creating a new PRODUCT record ===
curl -X POST -H "Content-Type: application/json" -d "{\"product_id\": \"p456\", \"name\": \"Smartphone\", \"price\": 299.99, \"description\": \"A powerful smartphone\", \"stock_quantity\": 50, \"user_id\": \"u123\", \"category_id\": \"C1\"}" %BASE_URL%/product
echo.
echo --------------------------

echo === Fetching all USER records ===
curl -X GET %BASE_URL%/user
echo.
echo --------------------------

echo === Fetching user 'u123' ===
curl -X GET %BASE_URL%/user/u123
echo.
echo --------------------------

echo === Updating user 'u123' ===
curl -X PUT -H "Content-Type: application/json" -d "{\"username\": \"john_doe_updated\", \"password\": \"secret\", \"email\": \"john_updated@example.com\"}" %BASE_URL%/user/u123
echo.
echo --------------------------

echo === Fetching all PRODUCT records ===
curl -X GET %BASE_URL%/product
echo.
echo --------------------------

echo === Fetching product 'p456' ===
curl -X GET %BASE_URL%/product/p456
echo.
echo --------------------------

echo === Updating product 'p456' ===
curl -X PUT -H "Content-Type: application/json" -d "{\"name\": \"Smartphone Pro\", \"price\": 349.99, \"description\": \"An upgraded smartphone\", \"stock_quantity\": 45, \"user_id\": \"u123\", \"category_id\": \"C1\"}" %BASE_URL%/product/p456
echo.
echo --------------------------

echo === Deleting product 'p456' ===
curl -X DELETE %BASE_URL%/product/p456
echo.
echo --------------------------

echo === Deleting seller 'u123' ===
curl -X DELETE %BASE_URL%/seller/u123
echo.
echo --------------------------

echo === Deleting category 'c101' ===
curl -X DELETE %BASE_URL%/category/c101
echo.
echo --------------------------

echo === Deleting user 'u123' ===
curl -X DELETE %BASE_URL%/user/u123
echo.
echo --------------------------
pause
