#written by Philip Pounds

import pandas as pd

A_L = []
A_S = []
A_T = []
d_theta = []

long_shear = []
short_shear = []

Pi = 3.14159265359
D_long_list = [] #inches
D_short_o_list = [] #inches
D_short_i_list = [] #inches
max_shear = 38000 #psi
G = 11.6*(10**6) #psi
fos = 2.5 #factor of safety
D_dx = 0.0625 # delta inches
D_L=  0.0625 #inches
D_S_O =  0.0625 #inches
D_S_I =  0 #inches
D_theta = 1.5*(3.14159265359/180) #rad
T = 14180.70543 #lbf-in
L_S = 26 #in
L_L = 38 #in


while(D_L<7):
    D_S_O =  0.125 #inches 
    D_L_shear_pass = False
    D_L=D_L+D_dx
    c =(D_L/2)
    j=(Pi/2)*(c**4)
    tau_l = fos*((T*c)/j)
    
    if(tau_l<max_shear):
        D_L_shear_pass = True

    while(D_S_O<7):
        D_S_I =  0 #inches
        D_S_O = D_S_O + D_dx
        D_S_angle_pass = False
        D_S_shear_pass = False
        c_o =(D_S_O/2)
        while(D_S_I<D_S_O-D_dx):
            D_S_shear_pass = False
            c_i =(D_S_I/2)
            j_s = (Pi/2)*((c_o**4)-(c_i**4))
            tau_2= fos*((T*c_o)/(j_s))
            
            if(tau_2<max_shear):
                D_S_shear_pass = True

            theta = ((T*L_S)/(j_s*G))-((T*L_L)/(j*G)) #short - long
            
            if abs((theta))<abs((D_theta)):
                D_S_angle_pass = True
            
            

            if D_S_shear_pass == True and D_S_angle_pass == True and D_L_shear_pass == True:
                D_long_list.append(D_L)
                D_short_o_list.append(D_S_O)
                D_short_i_list.append(D_S_I)
                d_theta.append(theta*(180/Pi))       
                        
                        
                Area_long = (Pi/2)*((D_L/2)**2)*38
                Area_short = ((Pi/2)*(((D_S_O/2)**2)-(D_S_I/2)**2))*26
                Area_total = Area_short+Area_long
                
                A_L.append(Area_long)
                A_S.append(Area_short)
                A_T.append(Area_total)
                
                long_shear.append(tau_l)
                short_shear.append(tau_2)
            
            D_S_I = D_S_I + D_dx
       
                    
                    


df = pd.DataFrame({
    "Long Shaft Diameter": D_long_list,
    "Short Shaft Outer Diameter": D_short_o_list,
    "Short Shaft Inner Diameter": D_short_i_list,
    "Long Shaft volume": A_L,
    "Short Shaft volume": A_S,
    "Both Shafts total volume": A_T,
    "Long Shaft Shear Stress": long_shear,
    "Short Shaft Shear Stress": short_shear,
    "Theta": d_theta
})


df_sorted = df.sort_values(by="Both Shafts total volume")
df_sorted.to_csv('shaft_properties.csv', index=False)