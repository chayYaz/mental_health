#visualization
import matplotlib.pyplot as plt
import pandas as pd

def plot2(df, condition1, condition2,subject,col_subject):

   # Filter data for the conditions
    condition1_data = df[df.index.str.contains(condition1, case=False, na=False)]
    condition2_data = df[df.index.str.contains(condition2, case=False, na=False)]

    # Create subplots
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Plot for condition1
    axes[0].plot(condition1_data.columns, condition1_data.iloc[0], label=condition1)
    axes[0].set_title(f'{subject} in {condition1}')
    axes[0].set_xlabel(col_subject)
    axes[0].set_ylabel(f'{subject} Level')
    axes[0].legend()

    # Plot for condition2
    axes[1].plot(condition2_data.columns, condition2_data.iloc[0], label=condition2, color='orange')
    axes[1].set_title(f'{subject} in {condition2}')
    axes[1].set_xlabel(col_subject)
    axes[1].set_ylabel(f'{subject} Level')
    axes[1].legend()

    # Display the plots
    
    file_name = f"{subject} By {col_subject}.png"
    plt.savefig(file_name, bbox_inches='tight')  # Save with tight layout
    plt.tight_layout()
    plt.show()

    



