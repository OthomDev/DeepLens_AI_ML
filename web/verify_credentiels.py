import user_exists as u
from verify_pw import verify_pw
import generate_return_dictionary as g



def verify_credentiels(username, password):
    if not u.user_exists(username):
        return g.generate_return_dictionary(301, "Invalid Username"), True
    
    correct_pw = verify_pw(username, password)

    if not correct_pw:
        return g.generate_return_dictionary(302, "Invalid Password"), True
    
    return None, False

