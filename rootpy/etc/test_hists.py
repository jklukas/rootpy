import ROOT
from random import seed, gauss
from array import array

seed(0)    # set a specific seed to get consistent random numbers

nhists = 4
nentries = 5000
sigma = 5.
xvals_list = [[gauss(0., sigma) for j in xrange(nentries)]
              for i in xrange(nhists)]
xvals1 = xvals_list[0]
#xvals1 = [gauss(0., sigma) for i in xrange(nentries)]
#xvals2 = [gauss(0., sigma) for i in xrange(nentries)]

outfile = ROOT.TFile('testfile.root', 'recreate')

dmeans = outfile.mkdir('means')
dscales = outfile.mkdir('scales')
dgaps = outfile.mkdir('gaps')
deffs = outfile.mkdir('efficiencies')
ddim = outfile.mkdir('dimensions')
dgraphs = outfile.mkdir('graphs')

for i in xrange(nhists):
    xvals = xvals_list[i]
    histnum = i + 1
    histtitle = "Histogram %i; x; Entries" % histnum

    dmeans.cd()
    hist = ROOT.TH1F("hist%i" % histnum, histtitle, 20, 0, (nhists + 1) * 10)
    map(hist.Fill, (x + 10 * histnum for x in xvals))
    hist.Write()
    del hist

    dscales.cd()
    hist = ROOT.TH1F("hist%i" % histnum, histtitle, 20, -20, 20)
    map(hist.Fill, xvals, (histnum for j in xrange(nentries)))
    hist.Write()
    del hist

    dgaps.cd()
    hist = ROOT.TH1F("hist%i" % histnum, histtitle, 20, -20, 20)
    map(hist.Fill, (x for x in xvals if abs(x) > 3))
    hist.Write()
    del hist

    deffs.cd()
    hist = ROOT.TH1F("hist%i" % histnum, histtitle, 20, -20, 20)
    map(hist.Fill, [x for (j, x) in enumerate(xvals1) if j % histnum == 0])
    hist.Write()
    del hist

for i in xrange(nhists - 1):
    histnum = i + 2

    deffs.cd()
    numerator = deffs.Get('hist%i' % histnum)
    denominator = deffs.Get('hist%i' % 1)
    graph = ROOT.TGraphAsymmErrors()
    graph.Divide(numerator, denominator)
    graph.SetTitle('Efficiency %i vs. 1; x; Efficiency' % histnum)
    graph.SetName('eff%iv1' % histnum)
    deffs.Append(graph)
    del graph

if True:
    ddim.cd()
    
    hist = ROOT.TH2F('hist2d', '2D Histogram', 10, -20., 20., 10, -10., 10.)
    map(hist.Fill, xvals_list[0], xvals_list[1])
    hist.Write()
    del hist

    hist = ROOT.TH3F('hist3d', '3D Histogram',
                     5, -20., 20., 5, -10., 10., 5, -5., 5.)
    map(hist.Fill, *xvals_list[:3])
    hist.Write()
    del hist

if True:
    dgraphs.cd()
    npoints = 10
    ints = array('f', range(npoints))
    values = array('f', xvals1[:npoints])
    halferrs = array('f', (0.5 for j in xrange(npoints)))
    fullerrs = array('f', (1.0 for j in xrange(npoints)))

    graph = ROOT.TGraph(npoints, ints, values)
    graph.SetTitle('A TGraph')
    graph.SetName('tgraph')
    dgraphs.Append(graph)
    del graph

    graph = ROOT.TGraphErrors(npoints, ints, values, halferrs, fullerrs)
    graph.SetTitle('A TGraphErrors')
    graph.SetName('tgrapherrors')
    dgraphs.Append(graph)
    del graph

    graph = ROOT.TGraphAsymmErrors(npoints, ints, values,
                                   halferrs, halferrs,
                                   fullerrs, halferrs)
    graph.SetTitle('A TGraphAsymmErrors')
    graph.SetName('tgraphasymmerrors')
    dgraphs.Append(graph)
    del graph

    graph = ROOT.TGraph2D(50, ints*5, ints*5, ints*5)
    graph.SetTitle('A TGraph2D')
    graph.SetName('tgraph2d')
    dgraphs.Append(graph)
    del graph

outfile.Write()
outfile.Close()
