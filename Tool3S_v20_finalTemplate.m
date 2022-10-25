% Carbon in Forest, in Building and Substitution
% This module calculates amount of carbon 
% stored in a building.
% to be harvested for this building and associated carbon emissions
% and floor area of buildings to be built from harvested wood
function Tool3S_v20
filestorage='3Soutput_Template.txt'; %output file name

% INPUT DATA -------------------------------------------------------------
% FOREST
aHarvest=0.74; 		%ha harvested area
biomass_left=0.1; 	% 10% (default) of harvested biomass is left on site to provide nutrients for regeneration and 90% is roundwood used in manufacturing
accRate=[3.3 5 6.7]; %MgC or t per ha per year carbon accumulation rate in Carreabian pine plantation
% MANUFACTURING
woodUsed=0.5; 	% 50% (default) of roundwood is assumed to be used for material production
materialUsed=1; % 100% (default) of prefabricated material is used in construction 
Dmnf1= 0; 	%km land transport distance 1 
Dmnf2= 0;	%km land transport distance 2 
Dmnf3=0;	%km sea transport distance 1 
Dmnf4=200; 	%km land transport distance 3 e.g., from the material manufacturing facilities to the construction site
% BUILDING
floor_area=18; 	% m2 floor area of one house
xl=20; 			% years expected life span of the building
% Material Intenisty [t/m2]
%Set 1
%Lightframe housing, one floor houses in Uganda
massARlm=0.108;   	% dreid timber or lumber
massARvn=0;         % plywood
massARstlT=0.00043;    %steel in pilot house construction
massARconT=0.02347;   %concrete in pilot house construction
% alternative for lightframe housing in Uganda
massARbrick=0.348+0.313;   % bricks
massARcon=0.076+0.375;   % reinforced concrete
%Set 2
% Midrise generic building from Churkina et al. 2020
massARmt_ps_co=0.209;   % primary structure commertial mid-rise generic Table 2
massARmt_ps_rs=0.194;   % primary structure residential mid-rise generic Table 2
massARmt_en_co=0.06;    % enclosure timber commertial mid-rise generic Table 3
massARmt_en_rs=0.028;   % enclosure timber residential mid-rise generic Table 3
massARwfb_en_co=0.021;  % enclosure wood fiber structure commertial mid-rise generic Table 3
massARwfb_en_rs=0.01;   % enclosure wood fiber structure resudential mid-rise generic Table 3
% composite system Table 2
massARcon_ps_co=0.608;   % primary structure commertial concrete mid-rise generic
massARstl_ps_co=0.083;   % primary structure commertial steel mid-rise generic
massARstl_en_co=0.01;     % enclosure steel mid-rise generic
massARfbg_en_co=0.002;   % enclosure fiberglass mid-rise generic
massARgyp_en_co=0.013;     % enclosure gypsum mid-rise generic
massARxps_en_co=0.002;   % enclosure XPS mid-rise genericformat bank % set output format
% END OF INPUT DATA ------------------------------------------------------

% PARAMETER LIST ----------------------------------------------------------
%Constants
cfLOG=0.5; % fraction of carbon in wood 
c2co2=3.67; % tons of CO2 associated with one ton of carbon
% CO2 EMISSION coefficients for materials [t CO2 eq/t material]
kLMs  =[0.12 0.12 0.12];     % softwood dried lumber low intensity production, Ruuska
kLMh  = [0.16 0.21 0.26];    % hardwood dried lumber low intensity production, Ruuska report
kMT   =[0.2 0.44 0.72];  % mass timber Table 6 from Pomp. and Montcaster 2018
kWFB  =[0.24 0.24 0.24];    % wood fiber Table 4 wood fiber from Ruuska report
kVN   =[0.3 0.35 0.409];       % Ökobaudat, mean, OSB Table 6 from Pomp. and Montcaster 2018
kSTL  =[1.34 2.11 3.81];   %steel from Pomp. and Montcaster 2018
kCON  =[0.033 0.145 0.295]; %concrete from Pomp. and Montcaster 2018
kFBG  =[3.15 3.15 3.15];    % fiberglass, Ruuska
kGYP  =[1.97 1.97 1.97];    %gypsum, Ruuska
kXPS  =[3.3 3.3 3.3];       %Polystyrene XPS, Ruuska
kBRK  =[0.179 0.225 0.354];     % brick all values from ICE DB V3.0 (Clay_Bricks sheet of excell)
% CO2 EMISSION coefficients for transport [t CO2 eq/t material]
kTruck = [0.00017398 0.00036024 0.00055731]; % 17t, 7.5-17t, 3.5-7.5t truck Table 6 from de Wolf et al 2017
kSea= 0.000013155; % sea cargo Table 6 from de Wolf et al 2017
% END of PARAMETERS LIST--------------------------------------------------

% CALCULATIONS START
% Declear functions nested in this program
f1=@buildingCstore;
f2=@buildingCemiMT;
f3=@buildingCemiSC;
f4=@woodDemand;
f5=@accumC;
f6=@forestCrecov;
f7=@forestCaccum;
f8=@buildingArea;
f9=@transportCemiMT;
%Conventional Building
WmaterialsINBuilding=(massARcon+massARbrick)*floor_area; %t weight of materials in conventional building
% Calculate carbon storage in timber building and carbon needed to be
% extracted from forest or demand for carbon
CstoredINBuilding=f1(floor_area); %t carbon stored in building
CstoredINMaterials=CstoredINBuilding/materialUsed; % t C stored in materials before construction
CstoredINRoundwood=CstoredINMaterials/woodUsed; %tC stored in roundwood brought to the plant
CneededFORBuilding=CstoredINRoundwood/(1-biomass_left);  %tC stored in harested trees
% Afforestation calculations: carbon accumulated over X years,
 % estimation of builings numbers to be built from harvest
    %CaccumForest=f7(aForest,xYears,1);  % carbon accumulated in forest area (aForest) after xYears
    %Charvested=CaccumForest*cfHarvest*aHarvest/aForest; %carbon harvested after xYears from a subsection of replanted area
    %NumberOfBuildings=Charvested/CneededFORBuilding;% number of buildings which can be built from harvested wood
 %End of Afforestation calculation% Calculate building weight
CaccumForest=0;   
NumberOfBuildings=1; % number of buildings to be built from harvested wood
Charvested=CneededFORBuilding;
Cbuildings= NumberOfBuildings*CstoredINBuilding; % tCstored in buildings constructed from harvested wood
Charvest2Scrap=CstoredINRoundwood -Cbuildings;    % tC stored in scrap wood from material manufacturing and construction
Charvest2Forest=CneededFORBuilding*biomass_left; % tC returuned to forest
BuildingAreaBuilt=NumberOfBuildings*floor_area; % floor area of constructed buildings
%Calculate time to replanish carbon debt in a forest
YearsToRegrowForest=f5(CneededFORBuilding,aHarvest,1)
CrecoveredForest=f6(xl,aHarvest,1)
%WRITE RESULTS TO a FILE
fileID=fopen(filestorage,'w');
%Calculations for min, mean, and max CO2 emissions values
for i=1:3
    fprintf(fileID,'%10s %d\n','Scenario', i);
    fprintf(fileID,'%10s %10s %10s %10s %10s %10s\n', 'Unit', 'Accumulated', 'Harvested', 'C2Scrap', 'C2Forest', 'C2Buildings');
    fprintf(fileID,'%10s %10.2f %10.2f %10.2f %10.2f %10.2f\n', 'tC',  CaccumForest, Charvested, Charvest2Scrap, Charvest2Forest, Cbuildings);
    fprintf(fileID,'%10s %10.2f %10.2f %10.2f %10.2f %10.2f\n', 'tCO2',  CaccumForest*c2co2, Charvested*c2co2, Charvest2Scrap*c2co2,  Charvest2Forest*c2co2, Cbuildings*c2co2);
    fprintf(fileID,'%10s %10.2f %10s\n','Buildings floor area:', BuildingAreaBuilt, 'm2');
    fprintf(fileID,'%10s %10.2f\n','Number of Buildings:', NumberOfBuildings);
    %
    % Calculate carbon emissions from builing production and material
    % transport
    CemittedBuildingTimber= f3(BuildingAreaBuilt,massARconT,massARstlT,0,i)+f2(BuildingAreaBuilt,i);
    CemittedBuildingSteelConcrete=f3(BuildingAreaBuilt,massARcon,0,massARbrick,i);
    CemittedTransportTimber=f9(Charvested/cfLOG,Dmnf1,kTruck(i))+f9(CstoredINRoundwood/cfLOG,Dmnf2,kTruck(i))+f9(CstoredINMaterials/cfLOG,Dmnf3,kSea)+f9(CstoredINBuilding/cfLOG,Dmnf4,kTruck(i));
    CemittedTransportConven=f9(WmaterialsINBuilding,Dmnf4,kTruck(i));
    fprintf(fileID,'%10s %10s %10s %10s %10s %10s\n', 'Unit', 'MassTimber','MT transport', 'SteelConcrete', 'SC transport','Difference');
    fprintf(fileID,'%10s %10.2f %10.2f %10.2f %10.2f %10.2f\n','tC',CemittedBuildingTimber,CemittedTransportTimber, CemittedBuildingSteelConcrete, CemittedTransportConven, CemittedBuildingSteelConcrete-CemittedBuildingTimber);
    fprintf(fileID,'%10s %10.2f %10.2f %10.2f %10.2f %10.2f\n','tCO2',CemittedBuildingTimber*c2co2,CemittedTransportTimber*c2co2, CemittedBuildingSteelConcrete*c2co2,  CemittedTransportConven*c2co2, (CemittedBuildingSteelConcrete-CemittedBuildingTimber)*c2co2);
    fprintf(fileID,'\n');
end
% CALCULATIONS END -------------------------------------------------------

% FUNCTIONS' DEFINITIONS -------------------------------------------------
% This function calculates amount of carbon stored in a building and
% amount of wood to be harvested for this building [t C]
    function y=buildingCstore(areaBLD) 
        y=(massARvn+massARlm)*areaBLD*cfLOG;
       % y=(massARmt_ps_co+massARmt_en_co+massARwfb_en_co)*areaBLD_co*cfLOG;
    end
% This function calculates floor area of buildings which can be constructed
% with given amount of wood
 function y=buildingArea(harvestedC) 
        y=harvestedC/cfLOG/(massARmt_ps_co+massARmt_en_co+massARwfb_en_co);
    end
% This function calculates amount of carbon emitted at the manufacturing
% stage of timber construction materials [t C] assuming all emissions are
% CO2
   function v=buildingCemiMT(areaBLD,ik)
        v=(massARlm*kLMh(ik)+massARvn*kVN(ik))*areaBLD/c2co2;
       %v=(massARmt_ps_co*kMT(1)+massARmt_en_co*kMT(1)+massARwfb_en_co*kWFB(1))*areaBLD_co/c2co2;
   end
% This function calculates amount of carbon emitted at the manufacturing
% stage of steel and concrete construction materials [t C]
    function z=buildingCemiSC(areaBLD,massconc, masssteal, massbrick, ik)
        z=(massconc*kCON(ik)+masssteal*kSTL(ik)+massbrick*kBRK(ik))*areaBLD/c2co2;
        %z2=(massARstl_en_co*kSTL(1)+massARfbg_en_co*kFBG(1)+massARgyp_en_co*kGYP(1)+massARxps_en_co*kXPS(1))*areaBLD/c2co2;
    end
%This function calculates amount of carbon emitted during transport
% stage of construction materials [t C] assuming all emissions are CO2
    function e=transportCemiMT(MatMass,distance,k)
        e=MatMass*distance*k/c2co2; % emissions from transport in [tC]
    end
% This function calculates wood needed to build timber building
    function w=woodDemand(carbonBLD)
        w=carbonBLD/woodUsed/materialUsed; % tonne of C total amount of carbon needed to build building including processing losses 
    end
% FUNCTIONS FOREST CARBON CALCULATIONS
% This function calculates number of years needed to accumulate harvested carbon
% using average carbon accumulation rate of a forest from the Cook-Paton
% database
    function yr=accumC(carbonHarv,areaHarv,yri)
        yr=carbonHarv/accRate(yri)/areaHarv; 
    end
% This function calculates amount of carbon recovered in the forest during the life time
% of a building
    function cr=forestCrecov(spanBLD,areaHarv,yri)
        cr=accRate(yri)*areaHarv*spanBLD;
    end
% This function calculates amount of carbon accumulated in the forest with
% area areaPlanted during a given period yrForest
function cacc=forestCaccum(areaPlanted,yrForest,yri)
        cacc=accRate(yri)*areaPlanted*yrForest;
    end
% END of FUNCTIONS DEFINITIONS-------------------------------------------
end