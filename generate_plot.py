import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition, mark_inset
from flask import Flask, Response,render_template
from io import BytesIO

# Flask app setup
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
matplotlib.use('agg')
# Simulate SOM weights and pose connections for demo purposes
loaded_som_distance_map_T=np.load("data/loaded_som_distance_map_T.npy")
pose_connections=np.load("data/pose_connections.npy")
som_weights=np.load("data/som_weights.npy")


# Function to generate and return the plot based on a selected cell (m, n)
def generate_plot(m, n):
    datax = som_weights[m, n]
    # Create the U-Matrix plot
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pcolor(loaded_som_distance_map_T, cmap='magma')
    ax.set_axis_off() 
    #fig.colorbar(ax.pcolor(loaded_som_distance_map_T, cmap='magma'), pad=0.)

    # Create inset plot
    parent_axes = plt.gca()
    ax2 = plt.axes([0, 0, 1, 1])
    ax2.plot([m - 1, m], [n - 1, n])
    ax2.set_xticks([])
    ax2.set_yticks([])

    # Plot pose connections
    ax3 = plt.gcf().add_axes([0, 0, 1, 1])
    for i in pose_connections:
        ax3.plot([datax[0, i[0]], datax[0, i[1]]], [-datax[1, i[0]], -datax[1, i[1]]], color='k', lw=1)
    ax3.set_xlim([0, 1])
    ax3.set_ylim([-1, 0])
    plt.xticks(visible=False)
    plt.yticks(visible=False)

    # Adjust inset position and mark it
    ip = InsetPosition(parent_axes, [0.7, 0.7, 0.3, 0.3])
    ax2.set_axes_locator(ip)
    ax3.set_axes_locator(ip)
    mark_inset(parent_axes, ax2, 2, 4, fc="none", ec="0.9")

    # Return the plot as a PNG image in a BytesIO buffer
    output = BytesIO()
    extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    plt.savefig(output, format='png',bbox_inches=extent, pad_inches=0)
    plt.close(fig)
    output.seek(0)
    return output


# Flask route to display the plot



@app.route('/')
def index():
    return render_template('index.html')


# Flask route to handle interactive plot updating based on clicks
@app.route('/click/<int:m>/<int:n>')
def click(m, n):
    # Generate and return plot based on clicked cell (m, n)
    buffer = generate_plot(m, n)
    return Response(buffer, mimetype='image/png')




if __name__ == '__main__':
    app.run(debug=True, port=8000)
