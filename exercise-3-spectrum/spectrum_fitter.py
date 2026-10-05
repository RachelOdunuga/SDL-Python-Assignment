
from scipy.optimize import curve_fit
import numpy as np 
import matplotlib.pyplot as plt
import sys

# defining function to use w/ curve_fit for fitting background

def parse_spectrum(filename):
    header = {}
    wavelengths = []
    fluxes = []
    current_key = None

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()

            if line.startswith("#"): # header key line
                key = line[1:].strip()
                if key not in ("DATA", ""):
                    current_key = key
                continue

            if current_key:    # header value line
                header[current_key] = line
                current_key = None
                continue

            if line.startswith("WAVELENGTH"): # skipping column header
                continue

            if "," in line:  # rows with data
                try:
                    w, fl = map(float, line.split(","))
                    wavelengths.append(w)
                    fluxes.append(fl)
                except ValueError:
                    pass

    return header, np.array(wavelengths), np.array(fluxes)


def polynomial(x, *params):
    """ a polynomial function to use for modelling spectra background"""
    return np.polyval(params, x) 

#also going to define Gaussian here for later 

def gaussian(x, amp, mu, sig, c_0):
    """
    A Gaussian function to use for fitting data using curvefit.
    x = x
    amp = amplitude
    mu = centre peak position
    sig = standard deviation
    c_0 = baseline
    """
    y = c_0 + amp * np.exp(-(x - mu)**2/(2*sig**2))
    return y 

# fitting background
#need to mask peak for fitting - going to use sigma clipping

def fit_function_bkg(w, f, deg, sig, max_iter, will_u_plot):
    """
    Fit a polynomial to background of spectra using sigma clipping, 
    plots the result, and prints parameters. 
    --------------------------------------------------------------
    w = wavelengths in Angstrom 
    f = flux 
    sig = adjust number of deviations / range of sigma clipping
    deg = desired degree of polynomial 
    max_iter = max number of iterations 

    """
    mask = np.ones_like(f, dtype=bool) #creating a mask of fluxes
    p0 = np.ones(deg + 1) # guess parameters for curve_fit

    for val in range(max_iter):
        popt, pcov = curve_fit(polynomial, w[mask], f[mask], p0=p0)
        p0 = popt # update guess for next iteration 

        fit = polynomial(w, *popt)

        residuals = f - fit

        std = np.std(residuals[mask])

        mask_sigclip = residuals >= (-sig * std)

        mask = mask_sigclip

    popt_bkg, pcov_final = curve_fit(polynomial, w[mask], f[mask], p0=p0)
    final_bkg = polynomial(w, *popt_bkg)

    if will_u_plot == True:
        plt.figure(figsize=(10,5))
        plt.scatter(w, f, label="Data")
        plt.plot(w, final_bkg, linewidth=2, color='orange', label="Background Fit")
        plt.legend()
        plt.grid(True)
        plt.xlabel("Wavelength (Angstrom)")
        plt.ylabel("Flux")
        plt.title("Background Fitting Result")
    print(f"The parameters for the background fit are: {popt_bkg}")
    print(f"The errors for the background fit's parameters are +/- {np.sqrt(np.diag(pcov_final))}")
    return popt_bkg, pcov_final, final_bkg 

# fitting peak

def fit_spectra(w, f, deg, sig, max_iter, plot):
    """
    A function that fits spectral peaks and background.
    This function relies on the "fit_function_bkg" function.
    ____________________________________________________
    w = wavelength data 
    f = flux data 
    deg = polynomial degree for background fit 
    sig = number of standard deviations for sigma clipping for background fit 
    max_iter = max number of iterations for background fitting 
    """
    popt_bkg, pcov_bkg, final_bkg = fit_function_bkg(w, f, deg, sig, max_iter, will_u_plot=False)

    bkg_subtracted = f - final_bkg

    #need to give guesses for initial parameters for a good fit - tried first time and got a straight line fit
    amp_guess = np.max(bkg_subtracted) # guessing amplitude as max value
    mu_guess = w[np.argmax(bkg_subtracted)] # guess for peak location where max is
    std_guess = np.std(f)
    c_0_guess = 0

    p0 = [amp_guess, mu_guess, std_guess, c_0_guess]

    popt, pcov = curve_fit(gaussian, w, bkg_subtracted, p0=p0)
    if plot == True:
        plt.figure(figsize=(10,5))
        plt.plot(w, f, label="Data")
        plt.plot(w, gaussian(w, *popt) + np.median(final_bkg), color = "red", label="Gaussian Result")
        plt.plot(w, final_bkg, color="orange", label="Background Fit Result")
        plt.xlabel(f"Wavelength (Angstrom)")
        plt.ylabel(r"Flux (erg s^{-1} cm^{-2})")
        plt.title("Spectra Fit Results")
        plt.grid(True)
        plt.legend()
    print(f"The parameters for the Gaussian fit are: {popt}")
    print(f"The errors for the Gaussian fit's parameters are +/- {np.sqrt(np.diag(pcov))}")
    print(f"The peak location is at {popt[1]} angstrom.")
    return popt, pcov

def main(file):
    header, wavelengths, fluxes = parse_spectrum(file)
    fit_spectra(wavelengths, fluxes, 1, 2, 5, plot=True)
    return 

if __name__ == '__main__':
    args = sys.argv[1:]
    main(args[0])
