def rsrp_to_percentage(rsrp):
    min_rsrp = -120
    max_rsrp = -50
    return max(0, min(100, ((rsrp - min_rsrp) / (max_rsrp - min_rsrp)) * 100))

# Example usage
rsrp = -105
percentage = rsrp_to_percentage(rsrp)
print(f"Signal Strength: {percentage}%")
