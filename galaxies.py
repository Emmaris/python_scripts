# Import libraries
import numpy as np
import matplotlib.pyplot as plt   #Used for plotting
from astropy.io import ascii      #Used for reading data tables
import os
from scipy import stats
from scipy.stats import linregress

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create a pause function for use throughout
import pdb
def pause():
    programPause = input("\n Interactive mode entered. Press the <Enter> to continue and c to exit interactive mode...")
    #code.interact(local=locals())
    pdb.set_trace()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Filename
filename = "C:/Users/Amy Soto/Desktop/demo/galaxy_iso_flux_allmetal.fout"

# Open the file with the SED fitting results of the UVUDF galaxies
tbl = ascii.read(filename)
data = np.array(tbl)
# To look at the data type - data.dtype.descr

# Name each data column with the names in title1
# Manually input column names
title1 = ['ID','Redshift','Tau','Metallicity','Age','Av','Mass','SFR','sSFR','la2t','chi2']
# Manually input column units
units1 = ['','','Log[Yr]','','Log[Yr]','','Log[$M_{\odot}$]','Log[$M_{\odot}/yr$]','Log[$Yr^{-1}$]','','']

# Create a loop to store data for each column in title1 names
for n in range(len(data[0])):
    vars()[title1[n]]=data[tbl.colnames[n]]

# Check length of each column for consistency
# Create an array to record the total number of elements for each column
num = np.zeros(len(tbl[0]))
print('\n Number of elements in each column:')
result = list(zip(title1, tbl))
for n in range(len(tbl[0])):
    print('\n '+title1[n]+':', len(data[tbl.colnames[n]]))
    num[n] = len(data[tbl.colnames[n]])

# Determine if identical number of elements in each column
if len(set(num)) == 1:
    print('\n Input columns have identical number of elements. Good to go!')
else:
    print('\n Data structure INVALID.  Number of column elements do not match!')
    pause()
#pause()
print('\n Now lets plot some of this data...')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Now lets create box plots to visualize Outliers
path = "C:/Users/Amy Soto/Desktop/demo/"
# could use os.getcwd() to get current working directory
directory = path+'boxplots/'
if not os.path.exists(directory):
    os.mkdir(directory)
# This will only select the variables I'm interested in, specifically:
# metallicity, age, extinction, mass, sfr, ssfr
for n in range(3,9):
    b = data[tbl.colnames[n]]
    plt.figure()
    plt.boxplot(b, meanline=True, showfliers=True)
    plt.title(title1[n]+' with Outliers')
    plt.ylabel(title1[n]+' ('+units1[n]+')')
    plt.savefig(directory+title1[n]+'.pdf',dpi=250,transparent=True)
    plt.show()
    #plt.close(fig=None)
print('\n Boxplots of original parameter inputs complete.')
print('\n Can use os.startfile(directory+plotname) to open pdf of plots')
title2 = ['Metallicity','Age','Av','Mass','SFR','sSFR']
print('\n plotname is Var1.pdf : ',title2)
pause()
plt.close(fig='all')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

print('\n Now to Identify Outliers and Clean Data')
# Now to Identify and Remove Outliers (Clean Data)
# First calculate the mean and median of the data sets
mnmx_data = np.zeros(shape=(len(tbl[0])-1,2))
mean_data = np.zeros(len(tbl[0])-1)
vari_data = np.zeros(len(tbl[0])-1)
stdv_data = np.zeros(len(tbl[0])-1)
skew_data = np.zeros(len(tbl[0])-1)
kurt_data = np.zeros(len(tbl[0])-1)
mnerr_dat = np.zeros(len(tbl[0])-1)
zscor_mass = np.array(len(tbl))
zscor_sfr = np.array(len(tbl))
zscor_age = np.array(len(tbl))
zscor_av = np.array(len(tbl))

for n in range(len(tbl[0])-1):
    data_stats = stats.describe(data[tbl.colnames[n+1]])
    if ((n+1) == 4) or ((n+1) == 6) or ((n+1) == 7) or ((n+1) == 8):
        data_stats = stats.describe(10.**data[tbl.colnames[n+1]])
    mnmx_data[n] = data_stats[1]
    mean_data[n] = data_stats[2]
    vari_data[n] = data_stats[3]
    skew_data[n] = data_stats[4]
    kurt_data[n] = data_stats[5]
    stdv_data[n] = np.std(data[tbl.colnames[n+1]])
    mnerr_dat[n] = stats.sem(data[tbl.colnames[n+1]])
    if ((n+1) == 4) or ((n+1) == 6) or ((n+1) == 7) or ((n+1) == 8):
        stdv_data[n] = np.std(10.**data[tbl.colnames[n+1]])
        mnerr_dat[n] = stats.sem(10.**data[tbl.colnames[n+1]])
    print('\nParameter: ', title1[n+1])
    print('Min, Max: ', mnmx_data[n])
    print('Mean: ', mean_data[n])
    print('Mean Error: ', mnerr_dat[n])
    print('Variance: ', vari_data[n])
    print('Std. Dev. (sigma): ', stdv_data[n])

# Find out how many sigma the values deviate from the mean
zscor_mass = np.abs(stats.zscore(10.**Mass))
zscor_sfr = np.abs(stats.zscore(10.**SFR))
zscor_age = np.abs(stats.zscore(10.**Age))
zscor_av  = np.abs(stats.zscore(Av))

# Now remove outliers with zscor_age, zscor_mass, zscor_sfr > thresh
thresh =  3.
print('\n zscore threshold is ',thresh)
out_mass = np.where(zscor_mass>thresh)
out_sfr = np.where(zscor_sfr>thresh)
out_age = np.where(zscor_age>thresh)
out_av = np.where(zscor_av>thresh)

comb_out1 = np.concatenate((out_mass,out_sfr,out_age), axis=None)
comb_out = np.concatenate((comb_out1,out_av), axis=None)

# Now to remove duplicates from list
comb_out.sort()
outliers = np.unique(comb_out)
out_ID = ID[outliers]
print('\n These are the Outliers - ')
print('\n Galaxy ID: ',out_ID)
print('\n Indices stored in "outliers" ')
pause()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create Clean Data arrays without Outliers
#title1 = ['ID','Redshift','Tau','Metallicity','Age','Av','Mass','SFR','sSFR','la2t','chi2']

cid = np.delete(ID, outliers)
cred = np.delete(Redshift, outliers)
ctau = np.delete(Tau, outliers)
cmetal = np.delete(Metallicity, outliers)
cage = np.delete(Age, outliers)
cav = np.delete(Av, outliers)
cmass = np.delete(Mass, outliers)
csfr = np.delete(SFR, outliers)
cssfr  = np.delete(sSFR, outliers)
cla2t = np.delete(la2t, outliers)
cchi2 = np.delete(chi2, outliers)

clean_data = [cid,cred,ctau,cmetal,cage,cav,cmass,csfr,cssfr,cla2t,cchi2]

print('')
print(len(data)-len(clean_data[0]),' Outliers were removed!')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Now lets analyze the data and create plots for clean data
print('\n Creating plots from cleaned data...')

# First create a directory for all these plots
path = "C:/Users/Amy Soto/Desktop/demo/"
# could use os.getcwd() to get current working directory
directory = path+'clean/'
if not os.path.exists(directory):
    os.mkdir(directory)

# Make Plots!!!
for n in range(1,9):
    x = clean_data[n]
    for j in range(1,9):
        if n == j :
            continue   # Prevents plots of identical parameters
        y = clean_data[j]
        plt.figure()
        plt.scatter(x,y)
        plt.title(title1[j]+' vs '+title1[n]+' of Clean Data Sample')
        plt.xlabel(title1[n]+' ('+units1[n]+')')
        plt.ylabel(title1[j]+' ('+units1[j]+')')
        #plt.show()
        plt.savefig(directory+title1[j]+'_'+title1[n]+'.pdf',dpi=250,transparent=True)
        plt.close(fig=None)
print('\n Plots of Clean Data complete.')
print('\n Can use os.startfile(directory+plotname) to open pdf of plots')
title2 = ['Redshift','Tau','Metallicity','Age','Av','Mass','SFR','sSFR']
print('\n plotname is Var1_Var2.pdf : ', title2)
pause()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Now lets analyze the data and create plots for SFG sample
print('\n I am interested in Star Forming Galaxies which have an SFR > 1.0 M_solar per year')
#title1 = ['ID','Redshift','Tau','Metallicity','Age','Av','Mass','SFR','sSFR','la2t','chi2']
isfr=np.where(clean_data[7] > 0.)
print('')
print(len(isfr[0]),' galaxies meet this criteria')

print('\n Creating plots for SFGs...')

# First create a directory for all these plots
path = "C:/Users/Amy Soto/Desktop/demo/"
# could use os.getcwd() to get current working directory
directory = path+'sfg/'
if not os.path.exists(directory):
    os.mkdir(directory)

# Create array with elements of interest
i_data = [cid[isfr],cred[isfr],ctau[isfr],cmetal[isfr],cage[isfr],cav[isfr],cmass[isfr],csfr[isfr],cssfr[isfr],cla2t[isfr],cchi2[isfr]]

# Output SFG sample to new filename
i_id = i_data[0]
dt = data.dtype.descr
dat = np.zeros(i_id.size, dtype=dt)

for i in range(0,11):
    dat[tbl.colnames[i]] = i_data[i]
np.savetxt('sfg_catalog.out', dat, header='ID,Redshift,Tau,Metallicity,Age,Av,Mass,SFR,sSFR,la2t,chi2', fmt = "%i %10.3f %10.3f %10.3f %10.3f %10.3f %10.3f %10.3f %10.3f %10.3f %10.3f")

# Make Plots!!!
for n in range(1,9):
    x = i_data[n]
    for j in range(1,9):
        if n == j :
            continue   # Prevents plots of identical parameters
        y = i_data[j]
        plt.figure()
        plt.scatter(x,y)
        plt.title(title1[j]+' vs '+title1[n]+' of SFG Sample')
        plt.xlabel(title1[n]+' ('+units1[n]+')')
        plt.ylabel(title1[j]+' ('+units1[j]+')')
        #plt.show()
        plt.savefig(directory+title1[j]+'_'+title1[n]+'.pdf',dpi=250,transparent=True)
        plt.close(fig=None)
print('\n Plots of SFGs complete.')
print('\n Can use os.startfile(directory+plotname) to open pdf of plots')
title2 = ['Redshift','Tau','Metallicity','Age','Av','Mass','SFR','sSFR']
print('\n plotname is Var1_Var2.pdf : ', title2)
pause()
# Can use os.startfile() to open pdf of plots

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# stats of SFGs
mnmx_idata = np.zeros(shape=(len(tbl[0])-1,2))
mean_idata = np.zeros(len(tbl[0])-1)
vari_idata = np.zeros(len(tbl[0])-1)
stdv_idata = np.zeros(len(tbl[0])-1)
skew_idata = np.zeros(len(tbl[0])-1)
kurt_idata = np.zeros(len(tbl[0])-1)
mnerr_idat = np.zeros(len(tbl[0])-1)
zscor_imass = np.array(len(isfr[0]))
zscor_isfr = np.array(len(isfr[0]))
zscor_iage = np.array(len(isfr[0]))
zscor_iav = np.array(len(isfr[0]))

for n in range(len(tbl[0])-1):
    data_stats = stats.describe(i_data[n+1])
    if ((n+1) == 4) or ((n+1) == 6) or ((n+1) == 7) or ((n+1) == 8):
        data_stats = stats.describe(10.**i_data[n+1])
    mnmx_idata[n] = data_stats[1]
    mean_idata[n] = data_stats[2]
    vari_idata[n] = data_stats[3]
    skew_idata[n] = data_stats[4]
    kurt_idata[n] = data_stats[5]
    stdv_idata[n] = np.std(i_data[n+1])
    mnerr_idat[n] = stats.sem(i_data[n+1])
    if ((n+1) == 4) or ((n+1) == 6) or ((n+1) == 7) or ((n+1) == 8):
        stdv_idata[n] = np.std(10.**i_data[n+1])
        mnerr_idat[n] = stats.sem(10.**i_data[n+1])
    print('\nParameter: ', title1[n+1])
    print('Min, Max: ', mnmx_idata[n])
    print('Mean: ', mean_idata[n])
    print('Mean Error: ', mnerr_idat[n])
    print('Variance: ', vari_idata[n])
    print('Std. Dev. (sigma): ', stdv_idata[n])

# Find out how many sigma the values deviate from the mean
#zscor_mass = np.abs(stats.zscore(10.**Mass))
#zscor_sfr = np.abs(stats.zscore(10.**SFR))
#zscor_age = np.abs(stats.zscore(10.**Age))
#zscor_av  = np.abs(stats.zscore(Av))
pause()
print('\n In particular I am interested in learning if there is a linear trend in the data which indicates a SFR Main Sequence')
print('\n So lets plot depending on redshift - ')
i_sfr=csfr[isfr]
i_mass=cmass[isfr]
i_red=cred[isfr]

k1=i_mass[np.where(i_red < 1.)]
k2=i_mass[np.where(i_red > 1.)]
z1=i_sfr[np.where(i_red < 1.)]
z2=i_sfr[np.where(i_red > 1.)]

fig=plt.figure()
ax=fig.add_subplot(111)
ax.scatter(k1,z1, c='b', label='z < 1')
ax.scatter(k2,z2, c='r', label='z > 1')
plt.title('SFR vs Mass of SFG Sample')
plt.xlabel('Mass [Log($M_{\odot}$)]')
plt.ylabel('SFR [Log($M_{\odot}/yr$)]')
plt.legend(loc='upper left')
plt.show()
plt.savefig(path+'SFR_Mass_red.pdf',dpi=250,transparent=True)
plt.close()

# Let's find the linear regression of this data
slope, intercept, r_value, p_value, std_err = stats.linregress(k1,z1)
mn = np.min(k1)
mx = np.max(k1)
x1 = np.linspace(mn,mx,500)
y1 = slope*x1+intercept
y1_1 = (slope*x1+intercept) + 3*std_err
y1_2 = (slope*x1+intercept) - 3*std_err
fig=plt.figure()
ax=fig.add_subplot(111)
ax.scatter(k1,z1, c='b', label='z < 1')
ax.scatter(k2,z2, c='r', label='z > 1')
ax.plot(x1,y1,'b', label='Linear Regression (z<1)')
ax.plot(x1,y1_1,'--b')
ax.plot(x1,y1_2,'--b')
plt.title('SFR vs Mass of SFG Sample')
plt.xlabel('Mass [Log($M_{\odot}$)]')
plt.ylabel('SFR [Log($M_{\odot}/yr$)]')
plt.legend(loc='upper left')
plt.show()
plt.savefig(path+'SFR_Mass_redreg.pdf',dpi=250,transparent=True)
plt.close()

print('\n slope : ',slope)
print('\n r-squared : ',r_value**2.)
print('\n standard deviation : ',std_err)

print('\n Linear Regression info : slope, intercept, r_value, p_value, std_err')
pause()
