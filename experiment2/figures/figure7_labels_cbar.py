from matplotlib.lines import Line2D
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Qt5Agg')

font = {'family' : 'Arial',
        'weight' : 'normal',
        'size'   : 24}

matplotlib.rc('font', **font)

cNorm = colors.Normalize(vmin=4, vmax=8)
cmap = matplotlib.cm.hot

fig, ax = plt.subplots()
cb1 = matplotlib.colorbar.ColorbarBase(ax, cmap=cmap, norm=cNorm, orientation='horizontal')
cb1.set_label('t-value')
ll, bb, ww, hh = cb1.ax.get_position().bounds
cb1.ax.set_xticks([4, 5, 6, 7, 8])
cb1.ax.set_position([ll*1.4, bb*1.15, ww*.85, hh*0.1])
fig.savefig('file_directory/plots/figure7/colorbar_wholeBrain.pdf', bbox_inches='tight')

custom_lines = [Line2D([0], [0], color='royalblue', label='anterior PHC', lw=16),
                Line2D([0], [0], color='crimson', label='posterior PHC', lw=16)]

legend = plt.legend(handles=custom_lines, frameon=False)
fig = legend.figure
fig.canvas.draw()
bbox = legend.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
plt.axis('off')
fig.savefig('file_directory/plots/figure7/phg_legend.pdf', bbox_inches=bbox)
