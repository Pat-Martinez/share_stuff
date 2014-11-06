
// Script to make it harder for webcrawlers to harvest email. For example, <a href="mailto:foo...example(dot)com">foo ... example dot com</a> will become
//     <a href="mailto:foo@example.com">foo@example.com</a>
$(function() {
$('a[href^="mailto:"]').each(function() {
this.href = this.href.replace('...', '@').replace(/\(dot\)/g, '.');
// Remove this line if you don't want to set the email address as link text:
this.innerHTML = this.href.replace('mailto:', '');
});
});


// Google Analytics
(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');

ga('create', 'UA-55827110-1', 'auto');
ga('send', 'pageview');


// Some test code that I'm playing around with.
$(function() {
$(".test").hide().show("slow");
});
