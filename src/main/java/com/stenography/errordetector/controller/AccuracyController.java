package com.stenography.errordetector.controller;

import com.stenography.errordetector.dto.AccuracyReport;
import com.stenography.errordetector.service.AccuracyService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

@RestController
@RequestMapping("/api/v1/accuracy")
public class AccuracyController {

    @Autowired
    private AccuracyService accuracyService;

    @PostMapping
    public ResponseEntity<AccuracyReport> assessAccuracy(
            @RequestParam("sourceFile") MultipartFile sourceFile,
            @RequestParam("targetFile") MultipartFile targetFile) {

        // Error handling for missing/empty files
        if (sourceFile.isEmpty() || targetFile.isEmpty()) {
            return new ResponseEntity<>(HttpStatus.BAD_REQUEST);
        }

        try {
            AccuracyReport report = accuracyService.assessTypingAccuracy(sourceFile, targetFile);
            return new ResponseEntity<>(report, HttpStatus.OK);
        } catch (IOException e) {
            // Log the exception
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
}