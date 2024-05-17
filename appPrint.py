import os

from utils.calcSiteTotals import calculate_site_totals
from utils.calcGrandTotals import calculate_grand_totals



# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
pdf_folder = os.path.join(current_dir, "uploads")

# Calculate site totals for each PDF file in the folder
calculate_site_totals(pdf_folder)

# Calculate grand totals for each site across all PDFs in the folder
calculate_grand_totals(pdf_folder)