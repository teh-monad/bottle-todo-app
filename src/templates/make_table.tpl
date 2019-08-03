% include('src/templates/header.tpl')
%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
	<ul>
	%for i in url():
		<li>{{!i}}</li>
	%end
	</ul>
	<p>The open items are as follows:</p>
	<table border="1">
	%for row in rows:
	  <tr>
	  %for col in row:
		<td>{{col}}</td>
	  %end
	  </tr>
	%end
	</table>
% include('src/templates/footer.tpl')
