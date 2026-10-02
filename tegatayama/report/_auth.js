if (!sessionStorage.getItem('suzuki_auth')) {
  var next = encodeURIComponent(location.href);
  location.replace('login.html?next=' + next);
}
