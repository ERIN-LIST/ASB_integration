# =================================================================================
# Apply functions to spacetime objects (from Edzer, version 0.5-0)
# =================================================================================
STapply = function(X, MARGIN, FUN, ...) {
  stopifnot(class(X) == "STFDF")
  if (MARGIN == "space" || MARGIN == 1)
    FOREACHSPACEapply(X, FUN, ...)
  else if (MARGIN == "time" || MARGIN == 2)
    FOREACHTIMEapply(X, FUN, ...)
  else stop("MARGIN should be 1 (space) or 2 (time)")	
}

FOREACHSPACEapply = function(X, FUN, ...) {
  ret = lapply(1:length(X@sp), function(i) FUN(X[i,], ...))
  #STFDF(X@sp, ret[[1]], do.call(rbind, ret))
}

FOREACHTIMEapply = function(X, FUN, ...) {
  ret = lapply(1:nrow(X@time), function(i) FUN(X[,i], ...))
}

# =================================================================================
# Seasonal Decomposition
# =================================================================================
require(raster)
# Get IDs for NA
Idx.na <- function(x){
  data   <- STapply(x, "space", function(i) i[,1])
  idx.na <- sapply(data, function(i) which(is.na(i)==TRUE)) 
  return(idx.na)
}

# Fill NA
FillNA<-function(x){
  idx.na <- unlist(Idx.na(x))
  if (length(idx.na)>0){
    x <- na.locf(x, na.rm=FALSE) # if first layer contains NA values, these are not replaced
    idx.na1 <- sort(unique(unlist(Idx.na(x))))
    if(length(idx.na1)>0){
      x <- na.locf(x, na.rm=FALSE, fromLast=TRUE)
    }
  }
  return(x)
}

# Convert into time-series
stl.convert <- function(x){
  data   <- STapply(x, "space", function(i) i[,1])
  ts1    <- lapply(data, function(i) ts(i[complete.cases(i)], start=c(2016, 1, 1), frequency = 32))
  stl1   <- lapply(ts1, function(i) stl(i[,1], "periodic"))
  return(stl1)
}

# Help function
stl.components <- function(x){
  res <- lapply(x, function(i) i["time.series"])
  res <- lapply(res, function(i) i["time.series"])
  res <- lapply(res, function(i) i[["time.series"]][, c("seasonal", "trend", "remainder")])
  return(res)
}

# Build result
stl.resultbuilder <- function(x, y){
  dat <- lapply(y, function(i) data.frame(i))
  vec <- unlist(sapply(dat, function(i) i[,"seasonal"]))
  vec <- as.vector(t(vec), mode='numeric')
  x@data$stl.seasonal <- vec
  vec <- unlist(sapply(dat, function(i) i[,"trend"]))
  vec <- as.vector(t(vec), mode='numeric')
  x@data$stl.trend <- vec
  vec <- unlist(sapply(dat, function(i) i[,"remainder"]))
  vec <- as.vector(t(vec), mode='numeric')
  x@data$stl.remainder <- vec
  return(x)
}

# Derive Decomposition
DECOMPOSITION <- function(x){
  res_stl <- stl.convert(x)
  res_components <- stl.components(res_stl)
  result <- stl.resultbuilder(x, res_components)
  return(result)
}
# ##-------------------------------------------------------------------------------------------
# ## End
# ##-------------------------------------------------------------------------------------------



# Example
library(raster)
library(spacetime)
library(xts)
library(pbapply)
library(forecast)
library(rgeos)

# Example scene: PROBAV_S10_TOC_X18Y02_20180721_333M_NDVI_V101_NDVI
data.folder <- "your-path-to-probav_X18Y02"
output.folder <- "your-path-to-probav_X18Y02"
setwd(data.folder)

files <- list.files()
files.time <- substr(files, 23, 30)
time <-as.POSIXct(files.time, format="%Y%m%d")

raster.stack <- stack(files)
r.ext <- raster(ext = extent(4, 4.25, 51.75, 52), res=res(raster.stack))
raster.brick.cropped <- crop(raster.stack, r.ext)
raster.brick.cropped <- setZ(raster.brick.cropped, time) 

myfdf <- as(raster.brick.cropped, "STFDF")
decomposition.result<-DECOMPOSITION(myfdf)

# Plot
stplot(decomposition.result[,,"stl.trend"])
stplot(decomposition.result[,,"stl.seasonal"])
stplot(decomposition.result[,,"stl.remainder"])
