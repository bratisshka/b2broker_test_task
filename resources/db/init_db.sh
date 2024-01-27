# Description: This script is used to initialize the database.
# It's purpose is to grant privileges to the user defined in the .env file to create and drop test databases.
# The problem is if env file is changed after the container is created, the changes are not reflected in the container.
# So you have to run this script manually after changing the env file.
# But I don't have enough time to fix this issue.
echo "GRANT ALL PRIVILEGES ON *.* TO '${MYSQL_USER}';"
mysql -e "GRANT ALL PRIVILEGES ON *.* TO '${MYSQL_USER}';" -uroot -p${MYSQL_ROOT_PASSWORD}