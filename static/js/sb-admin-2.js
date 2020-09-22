toggle = ()=>{
    a = document.getElementById('accordionSidebar')
    if (a.className.includes(' toggled'))
        a.className = a.className.replace(' toggled', '')
    else
        a.className+=' toggled'
}