// Scripts to make it harder for webcrawlers to harvest email. For example, <a href="mailto:foo(at)gmail(dot)com">foo at gmail dot com</a>
// will become <a href="mailto:foo@gmail.com">foo@gmail.com</a>
$(function() {
// To use for any <a href= that begins with "mailto" use $('a[href^="mailto:"]') instead of
// $('.email').
$('.email').each(function() {
this.href = this.href.replace('\(at\)', '@').replace(/\(dot\)/g, '.');
this.innerHTML = this.href.replace('mailto:', ''); // link text.
});
});

// Similar to above except doesn't show link text. For example, used this in footer.
$(function() {
$('.email-icon').each(function() {
this.href = this.href.replace('\(at\)', '@').replace(/\(dot\)/g, '.');
});
});


// Google Analytics
(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');

ga('create', 'UA-55827110-1', 'auto');
ga('send', 'pageview');


//****** Didn't use this option because was not an Unobtrusive solution ******
// Popup box to confirm deletion of an item. For example, 
// in template set button value to "{{ item.id }}"
//
// function confirmDelete(value) {
//   if (confirm("OK to Delete?")) {
//     var item_id = value;
//     parent.location= "/sharing/inventory/delete_item/" + item_id;
//   } 
// } 


// Popup box to confirm deletion of an item.
$(function(){
  $('.delete').click(function(){
    if (confirm("OK to Delete?")){
      parent.location= ($(this).attr('href'));
    }
    else {
      return false;
    }
  });
});
