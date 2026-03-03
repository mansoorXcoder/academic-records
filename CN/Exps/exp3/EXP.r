# -------------------------------
# Install required packages (run once)
# -------------------------------
if (!require(ggplot2)) install.packages("ggplot2", dependencies = TRUE)
if (!require(dplyr)) install.packages("dplyr", dependencies = TRUE)

# -------------------------------
# Load libraries
# -------------------------------
library(ggplot2)
library(dplyr)

# -------------------------------
# Load iris dataset
# -------------------------------
data("iris")

# -------------------------------
# 1. Simple Bar Chart (Species Count)
# -------------------------------
species_counts <- iris %>%
  group_by(Species) %>%
  summarise(Count = n(), .groups = "drop")

ggplot(species_counts, aes(x = Species, y = Count, fill = Species)) +
  geom_bar(stat = "identity") +
  labs(
    title = "Count of Observations per Iris Species",
    x = "Species",
    y = "Count"
  ) +
  theme_minimal()

# -------------------------------
# 2. Stacked Bar Chart (Species vs. Sepal Length Categories)
# -------------------------------
# Create categories for Sepal.Length
iris$SepalLengthCat <- cut(
  iris$Sepal.Length,
  breaks = c(4, 5, 6, 7, 8),
  labels = c("4-5", "5-6", "6-7", "7-8"),
  include.lowest = TRUE
)

# Count by Species and SepalLengthCat
stacked_counts <- iris %>%
  group_by(Species, SepalLengthCat) %>%
  summarise(Count = n(), .groups = "drop")

ggplot(stacked_counts, aes(x = Species, y = Count, fill = SepalLengthCat)) +
  geom_bar(stat = "identity") +
  labs(
    title = "Stacked Bar Chart of Sepal Length Categories per Species",
    x = "Species",
    y = "Count",
    fill = "Sepal Length Range"
  ) +
  theme_minimal()