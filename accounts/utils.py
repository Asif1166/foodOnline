def detectUser(user):
    if user.roll == 1:
        redirectUrl = 'vendorDashboard'
        return redirectUrl
    elif user.roll == 2:
        redirectUrl = 'custDashboard'
        return redirectUrl
    elif user.roll == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl