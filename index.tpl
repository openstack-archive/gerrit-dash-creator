<html>
  <head>
    <title>Openstack Reviews</title>
  </head>
  <body>
    <h1>Openstack Review Dashboards</h1>
    <ul>
    <%
    for url in urls: 
        %>
    <li><a href="{{url['url']}}" target="_blank">{{url['title']}}</a></li>
    <% end %>
    </ul>
  </body>
</html>
