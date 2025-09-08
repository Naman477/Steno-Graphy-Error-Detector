package com.stenography.errordetector.service;

import com.stenography.errordetector.dto.AccuracyReport;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class AccuracyService {

    public AccuracyReport assessTypingAccuracy(MultipartFile sourceFile, MultipartFile targetFile) throws IOException {
        String sourceText = readFileContent(sourceFile);
        String targetText = readFileContent(targetFile);

        List<String> sourceWords = tokenizeWords(sourceText);
        List<String> targetWords = tokenizeWords(targetText);

        // Calculate word-level differences and generate highlighted HTML
        StringBuilder highlightedSourceHtml = new StringBuilder();
        StringBuilder highlightedTargetHtml = new StringBuilder();
        List<String> differences = new ArrayList<>();
        long errorsFound = 0;
        long matchedWords = 0;

        int sourceIdx = 0;
        int targetIdx = 0;

        while (sourceIdx < sourceWords.size() || targetIdx < targetWords.size()) {
            String sourceWord = (sourceIdx < sourceWords.size()) ? sourceWords.get(sourceIdx) : null;
            String targetWord = (targetIdx < targetWords.size()) ? targetWords.get(targetIdx) : null;

            if (sourceWord != null && targetWord != null) {
                if (sourceWord.equals(targetWord)) {
                    matchedWords++;
                    highlightedSourceHtml.append(sourceWord).append(" ");
                    highlightedTargetHtml.append(targetWord).append(" ");
                } else {
                    errorsFound++;
                    differences.add(String.format("Mismatch: Source: \"%s\" | Target: \"%s\"", sourceWord, targetWord));
                    highlightedSourceHtml.append("<span class=\"diff-error\">").append(sourceWord).append("</span> ");
                    highlightedTargetHtml.append("<span class=\"diff-error\">").append(targetWord).append("</span> ");
                }
                sourceIdx++;
                targetIdx++;
            } else if (sourceWord != null) {
                // Word missing in target
                errorsFound++;
                differences.add(String.format("Missing in Target: \"%s\"", sourceWord));
                highlightedSourceHtml.append("<span class=\"diff-error\">").append(sourceWord).append("</span> ");
                highlightedTargetHtml.append("<span class=\"diff-missing\">[MISSING]</span> "); // Placeholder for missing word
                sourceIdx++;
            } else if (targetWord != null) {
                // Extra word in target
                errorsFound++;
                differences.add(String.format("Extra in Target: \"%s\"", targetWord));
                highlightedSourceHtml.append("<span class=\"diff-extra\">[EXTRA]</span> "); // Placeholder for extra word
                highlightedTargetHtml.append("<span class=\"diff-error\">").append(targetWord).append("</span> ");
                targetIdx++;
            }
        }


        long sourceTotalWords = sourceWords.size();
        double accuracyPercentage = 0.0;
        if (sourceTotalWords > 0) {
            accuracyPercentage = ((double) matchedWords / sourceTotalWords) * 100;
        }

        AccuracyReport report = new AccuracyReport();
        report.setSourceTotalChars(sourceText.length()); // Still report char count for context
        report.setErrorsFound(errorsFound);
        report.setAccuracy(String.format("%.2f%%", accuracyPercentage));
        report.setDifferences(differences);
        report.setHighlightedSourceHtml(highlightedSourceHtml.toString().trim());
        report.setHighlightedTargetHtml(highlightedTargetHtml.toString().trim());

        return report;
    }

    private String readFileContent(MultipartFile file) throws IOException {
        String content = new String(file.getBytes(), StandardCharsets.UTF_8);
        // Handle different line endings by normalizing to \n
        content = content.replace("\r\n", "\n").replace("\r", "\n");
        // Remove BOM if present
        if (content.startsWith("\uFEFF")) {
            content = content.substring(1);
        }
        return content;
    }

    private List<String> tokenizeWords(String text) {
        // Simple word tokenization: split by one or more whitespace characters
        // This will handle multiple spaces between words by treating them as a single delimiter.
        // Leading/trailing spaces will be removed by trim().
        return Arrays.asList(text.trim().split("\\s+"));
    }
}
