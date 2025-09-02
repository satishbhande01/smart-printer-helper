import streamlit as st
import main
from pdf_separator import separate_pdf_by_color
import os

# Page Config
st.set_page_config(page_title="Smart Printer Page Helper", page_icon="🖨️")

# Header
st.title("🖨️ Smart Printer Page Helper")
st.markdown("""
## 🧠 What This App Does

Welcome to **Smart Printer Page Helper** — your assistant for smarter and more cost-efficient printing!  
This tool helps you easily:

- **Select and organize color and black & white pages** from your documents.
- **Manually pick** colored pages or
- **Automatically detect** them from a PDF using intelligent color analysis.
- Prepare your print jobs to **avoid unnecessary color printing** and **save ink & money**.

Whether you're printing assignments, reports, or slides — we've got your back! 🎯

---

### ⚠️ Disclaimer on Auto-Detection

The **automatic detection feature** uses a color sensitivity setting to estimate whether a page contains color.  
While it works well in most cases, **results may vary** depending on PDF quality, images, and highlights.

We recommend reviewing the results before finalizing your print job.
""")


st.divider()

# ========== Manual Page Selection ==========
st.header("📄 Step 1: Enter Total Pages")
pages = st.number_input("Total Number of Pages", min_value=1, step=1)

st.header("🎨 Step 2: Select Colored Pages")
tog = st.toggle("🔄 Use comma-separated values instead", help="Use '1,2,3' or '1-5,7' style input")
bwc = ""

if not tog:
    selected = st.multiselect(
        "Choose the colored or B/W pages from the list below:",
        options=[i for i in range(1, pages + 1)],
        placeholder="Pick one or more pages..."
    )
    if selected:
        bwc = ",".join(map(str, selected))
else:
    bwc = st.text_input(
        "Enter Page Numbers (comma-separated)",
        placeholder="Example: 1,2,3,5-7",
        help="Use commas and hyphens to define ranges"
    )

st.divider()
st.header("🧾 Step 3: Get Remaining Pages")

if st.button("Submit"):
    if bwc:
        try:
            #For Colored Pages
            colored = main.PrinterString(pages, bwc)
            colored_result = colored.printer_str()
            #For B/W pages
            bw = main.PrinterString(pages, colored_result)
            bw_result = bw.printer_str()
            #Outputs
            st.badge("Colored Pages",color="green")
            st.code(colored_result, language="")  # No language needed, just plain text
            st.badge("Black and White Pages",color="blue")
            st.code(bw_result, language="")

        except Exception as e:
            st.error(f"⚠️ Error processing input: {e}")
    else:
        st.info("Please provide input to view remaining pages.")


# ========== Optional: PDF Color Splitter ==========
st.divider()
with st.expander("🧪 Optional: Automatically Detect Colored Pages from PDF"):
    st.markdown("Upload a PDF and let the tool split it into color and B&W pages.")

    uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])
    threshold_level = st.selectbox(
    "Color Detection Sensitivity",
    options=["Strict (Few pages detected as color)", 
             "Balanced (Recommended)", 
             "Loose (More pages detected as color)"],
    index=1
    )

    # Map to actual float values
    threshold_map = {
        "Strict (Few pages detected as color)": 0.0005,
        "Balanced (Recommended)": 0.001,
        "Loose (More pages detected as color)": 0.005
    }

    threshold = threshold_map[threshold_level]


    if uploaded_pdf:
        st.caption("Lower threshold = more strict color detection.")

        if st.button("🎯 Process PDF"):
            with open("uploaded.pdf", "wb") as f:
                f.write(uploaded_pdf.read())

            st.info("Processing...")

            try:
                color_path, bw_path = separate_pdf_by_color("uploaded.pdf", threshold)

                if not color_path and not bw_path:
                    st.warning("No pages were detected in either category. Try adjusting the threshold.")
                else:
                    st.success("Done! Download your files below:")

                    if color_path:
                        with open(color_path, "rb") as f:
                            st.download_button("⬇️ Download Color Pages", f, file_name=color_path)
                    if bw_path:
                        with open(bw_path, "rb") as f:
                            st.download_button("⬇️ Download B&W Pages", f, file_name=bw_path)

                os.remove("uploaded.pdf")
            except Exception as e:
                st.error(f"❌ Failed to process PDF: {e}")
