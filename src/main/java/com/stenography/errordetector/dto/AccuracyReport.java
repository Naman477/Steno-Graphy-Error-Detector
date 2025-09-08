package com.stenography.errordetector.dto;

import java.util.List;

public class AccuracyReport {
    private long sourceTotalChars;
    private long errorsFound;
    private String accuracy;
    private List<String> differences;
    private String highlightedSourceHtml;
    private String highlightedTargetHtml;

    public AccuracyReport() {
    }

    public AccuracyReport(long sourceTotalChars, long errorsFound, String accuracy, List<String> differences) {
        this.sourceTotalChars = sourceTotalChars;
        this.errorsFound = errorsFound;
        this.accuracy = accuracy;
        this.differences = differences;
    }

    public long getSourceTotalChars() {
        return sourceTotalChars;
    }

    public void setSourceTotalChars(long sourceTotalChars) {
        this.sourceTotalChars = sourceTotalChars;
    }

    public long getErrorsFound() {
        return errorsFound;
    }

    public void setErrorsFound(long errorsFound) {
        this.errorsFound = errorsFound;
    }

    public String getAccuracy() {
        return accuracy;
    }

    public void setAccuracy(String accuracy) {
        this.accuracy = accuracy;
    }

    public List<String> getDifferences() {
        return differences;
    }

    public void setDifferences(List<String> differences) {
        this.differences = differences;
    }

    public String getHighlightedSourceHtml() {
        return highlightedSourceHtml;
    }

    public void setHighlightedSourceHtml(String highlightedSourceHtml) {
        this.highlightedSourceHtml = highlightedSourceHtml;
    }

    public String getHighlightedTargetHtml() {
        return highlightedTargetHtml;
    }

    public void setHighlightedTargetHtml(String highlightedTargetHtml) {
        this.highlightedTargetHtml = highlightedTargetHtml;
    }
}