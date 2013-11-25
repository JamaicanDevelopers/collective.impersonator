collective.impersonator
=======================

"Olisi kätevää jos ylläpitäjänä olisi mahdollista "tekeytyä" joksikin
käyttäjäksi ja nähdä mitä tämä sivustosta näkee. Toiminnon voisi aktivoida
lisäämällä X-impersonate HTTP headerin, jonka arvona on käyttäjätunnus. Tämän
toiminnon käyttäminen tarvitsisi myös pääkäyttäjä oikeuden autentikoidulta
käyttäjältä." -Jussi Talaskivi


Usage
-----

With Chrome:

- Install `Extra Headers`__ -plugin
- Log in as a Plone user in Administrators -group
- Enable header ``X-impersonate`` with the target user id
- Refresh the page

__ https://chrome.google.com/webstore/detail/extra-headers/afmemiddmafkejaokgicfnaeahejbhfj?hl=en

.. note:: *collective.impersonator* does not work with The default zope-admin
   -user (``admin`` or any other only defined in the Zope app root). This is
   be design, for your security.




