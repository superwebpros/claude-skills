#!/bin/bash
# READ-ONLY PHP exposure audit. Makes no changes.
echo "=== HOST: $(hostname) | $(. /etc/os-release 2>/dev/null; echo $PRETTY_NAME) | uptime: $(uptime -p 2>/dev/null)"
echo "=== HOST PHP BINARIES"
for b in $(ls /usr/bin/php* /usr/sbin/php-fpm* /usr/local/bin/php* /opt/*/bin/php 2>/dev/null | sort -u); do
  [ -x "$b" ] && echo "$b: $($b -v 2>/dev/null | head -1)"
done
command -v php >/dev/null && echo "default php: $(php -v | head -1)"
echo "=== PHP PACKAGES"
dpkg -l 2>/dev/null | awk '/^ii/ && $2 ~ /^php[0-9.]*(-fpm|-cli|-common)?$|^libapache2-mod-php/ {print $2, $3}'
echo "=== PHP-FPM / WEB SERVICES RUNNING"
systemctl list-units --type=service --state=running 2>/dev/null | grep -Ei 'php|nginx|apache|httpd|litespeed|caddy|openresty' | awk '{print $1}'
ps -eo comm,args 2>/dev/null | grep -Ei 'php-fpm: master|frankenphp|lsphp|php artisan|php -S' | grep -v grep | head
echo "=== LISTENING PUBLIC PORTS"
ss -tlnp 2>/dev/null | awk 'NR>1 {print $4, $6}' | grep -Ev '127\.0\.0\.1|\[::1\]' | sort -u | head -30
echo "=== SITES (nginx/apache vhosts)"
grep -rhoE 'server_name[^;]+' /etc/nginx/sites-enabled /etc/nginx/conf.d 2>/dev/null | sort -u | head -40
grep -rhoE 'ServerName\s+\S+' /etc/apache2/sites-enabled 2>/dev/null | sort -u | head -20
echo "=== WORDPRESS INSTALLS (wp-config.php)"
find / -xdev -maxdepth 6 -name wp-config.php -not -path '*/proc/*' 2>/dev/null | head -40
echo "=== DOCKER"
if command -v docker >/dev/null; then
  docker ps --format '{{.Names}}|{{.Image}}|{{.Ports}}' 2>/dev/null
  echo "--- PHP inside containers"
  for c in $(docker ps -q 2>/dev/null); do
    n=$(docker inspect -f '{{.Name}}' $c | tr -d /)
    v=$(docker exec $c sh -c 'command -v php >/dev/null && php -v 2>/dev/null | head -1 || (ls /usr/local/sbin/php-fpm /usr/sbin/php-fpm* 2>/dev/null | head -1)' 2>/dev/null)
    [ -n "$v" ] && echo "$n: $v"
  done
else echo "docker not installed"; fi
echo "=== PENDING PHP APT UPGRADES (from cached lists, no refresh)"
apt list --upgradable 2>/dev/null | grep -i '^php' | head -20
echo "=== PHP APT SOURCES"
grep -rhE 'ondrej|sury' /etc/apt/sources.list /etc/apt/sources.list.d 2>/dev/null | head -3
echo "=== DONE"
