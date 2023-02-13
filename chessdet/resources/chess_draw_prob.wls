#!/usr/bin/env wolframscript
(* ::Package:: *)

(*Approximate the draw prob where r1 \[Equal] r2*)
data={{-500,0.005},{0,0.02},{1500,0.2},{2100,0.4},{3900,0.9}};
f = Interpolation[data, InterpolationOrder->4]
quartic = Fit[data, {1,x,x^2,x^3,x^4}, x]
ListPlot[data];
Plot[
{
f[x],
0.01999999999999999` +0.000016937472249972676` x+6.744852369851588`*^-9 x^2+5.963211171544542`*^-11 x^3-1.221540804874144`*^-14
}
,{x,-500,3900}]



