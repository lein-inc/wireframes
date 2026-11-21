if (!sessionStorage.getItem('oumi_prop_auth')) {
  var next = encodeURIComponent(location.href);
  location.replace('login.html?next=' + next);
}
